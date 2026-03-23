---
title: "Making a Tiny Compute Clear Survive a Real Unreal Frame"
date: 2026-03-23
lastmod: 2026-03-23
draft: true
authors: ["Pawel Stolecki"]
description: "A practical path from a tiny Unreal-style compute clear pass to the D3D12 objects, bindings, barriers, and submission rules that make it survive a real frame."
tags: ["rendering", "gpu", "d3d12", "compute", "graphics-api"]
categories: ["analysis"]
summary: "A step-by-step walkthrough of what has to line up for one tiny compute clear pass to survive a normal Unreal-style frame: resource creation, views, root signature, PSO, command recording, submission, and synchronization."
showTableOfContents: false
keywords: ["D3D12 compute", "root signature", "descriptor heap", "UAV barrier", "CreateComputePipelineState", "Dispatch"]
---

{{< article-nav >}}

The shader is the easy part. One kernel. One output texture. One `Dispatch`. In isolation, that looks trivial.

In a real frame, trivial is not enough. The pass has to survive resource allocation, binding, command recording, queue submission, and the next pass that touches the same texture. That is where low-level graphics API work starts.

So this article is not about what compute shaders are. It is about what has to line up before one tiny compute clear pass survives a normal Unreal-style frame and becomes real GPU work in D3D12.

The pass is deliberately small: clear a texture through a compute shader. The goal is not the clear itself. The goal is to use that clear to expose the machinery that engines usually hide.

Why care about something this small?

- because this is the shortest path from "I added a compute pass" to "I understand why it works"
- because when a dispatch silently fails, the failure is usually in the machinery around it, not in the shader body
- because frame graphs, async compute, and later Vulkan mapping all sit on top of this same unit of work
- because if you mainly work in Unreal, this is the layer the engine is usually hiding for you

<div class="fg-reveal" style="margin:1.5em 0;border-radius:12px;overflow:hidden;border:1px solid var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);">
   <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;">
      <div style="padding:1em;text-align:center;border-right:1px solid var(--color-neutral-200,#e5e5e5);border-bottom:1px solid var(--color-neutral-200,#e5e5e5);">
         <div style="font-weight:800;font-size:.95em;">Make The Pass Real</div>
         <div style="font-size:.82em;opacity:.7;line-height:1.4;margin-top:.2em;">See every object that has to line up before one tiny compute clear becomes a legal dispatch</div>
      </div>
      <div style="padding:1em;text-align:center;border-right:1px solid var(--color-neutral-200,#e5e5e5);border-bottom:1px solid var(--color-neutral-200,#e5e5e5);">
         <div style="font-weight:800;font-size:.95em;">Debug The Failure Cases</div>
         <div style="font-size:.82em;opacity:.7;line-height:1.4;margin-top:.2em;">Turn "the pass vanished" into a concrete checklist: views, heaps, root signature, PSO, states, submission</div>
      </div>
      <div style="padding:1em;text-align:center;border-bottom:1px solid var(--color-neutral-200,#e5e5e5);">
         <div style="font-weight:800;font-size:.95em;">See Under Unreal</div>
         <div style="font-size:.82em;opacity:.7;line-height:1.4;margin-top:.2em;">Use a familiar Unreal-style pass as the entry point, then walk one layer down into D3D12</div>
      </div>
   </div>
</div>

---

## Why Read This

If you use Unreal, the friendly version of this story looks something like this:

- write a tiny compute shader
- create a texture the pass will write
- bind a small parameter block with the clear color
- add a pass to the frame
- dispatch it

That is the engine-facing story. The D3D12 story underneath is longer:

1. Which resources are visible to the shader, and as what kind of view?
2. How are those views exposed through the root signature?
3. Where do those descriptors live, and when are they safe to modify?
4. Which command list type records the work?
5. What resource state must each resource be in before and after dispatch?
6. When is the CPU allowed to recycle allocators, descriptors, or upload memory?

<div class="ds-callout ds-callout--warn" style="margin-top:.7em;padding:.55em .9em;font-size:.9em;font-style:italic;">
   In D3D12, the hard part is often not the kernel. It is making the dispatch legal.
</div>

That is the trade. Driver-side tracking goes down. Application-side responsibility goes up. The payoff is that binding, submission, and synchronization stop being opaque runtime magic and become systems you can reason about directly.

So the reader payoff here is practical, not academic.

- you can trace a familiar Unreal-style pass down to the D3D12 objects that actually make it run
- you get a debugging checklist for the usual "dispatch ran but the frame did not change" failure mode
- you get a cleaner mental model for later topics like frame graphs, async compute, and Vulkan mapping
- you stop treating compute as "shader plus `Dispatch`" and start seeing the frame machinery around it

---

## If You Mostly Use Unreal

Most people do not start with raw D3D12. They start in an engine.

In Unreal, compute usually shows up through higher-level rendering systems: a shader, a parameter struct, a render graph pass, and engine-managed resource lifetimes. The dispatch feels local. The machinery behind it does not.

That is exactly why this article exists. Unreal gives you a productive mental model. D3D12 is the same story with the cover removed.

So use this as the starting point:

> You are in Unreal. You want to add a tiny compute pass that clears a texture. The shader is trivial. The question is: what machinery sits underneath that pass by the time it reaches D3D12?

Use this translation layer while reading:

<div class="diagram-ftable">
<table>
   <tr><th>Engine-facing idea</th><th>What it usually feels like</th><th>D3D12 layer underneath</th></tr>
   <tr><td><strong>Compute shader class / shader asset</strong></td><td>The shader you compile and reference from engine code</td><td>Shader bytecode plus a compute PSO</td></tr>
   <tr><td><strong>RDG texture or bound output</strong></td><td>A texture the pass writes</td><td>A resource plus a UAV view</td></tr>
   <tr><td><strong>Shader parameter struct</strong></td><td>A friendly parameter block with textures, UAVs, and constants</td><td>Root signature layout plus descriptor tables or root constants</td></tr>
   <tr><td><strong>RDG pass execution</strong></td><td>The place where the pass is recorded and scheduled</td><td>Command list recording plus queue submission</td></tr>
   <tr><td><strong>Engine handles transitions</strong></td><td>The texture is just "ready" for the next step</td><td>Explicit resource transitions and UAV ordering barriers</td></tr>
   <tr><td><strong>Engine owns lifetime</strong></td><td>Resources and bindings seem to just exist when needed</td><td>Descriptor heap lifetime, allocator reuse rules, and fence-based ownership</td></tr>
</table>
</div>

You do not need to stop thinking like an Unreal user to follow the article. Just keep translating one layer down:

- "the engine bound a texture" becomes "a view was created and placed in a descriptor heap"
- "the engine dispatched a compute shader" becomes "a command list bound a root signature and PSO, then called `Dispatch`"
- "the engine handled synchronization" becomes "somebody inserted the transitions, ordering barriers, and fences"

That is the path we are walking here. Same pass, same intent, lower level. Think of the whole article as tracing one tiny Unreal-style compute clear all the way down to raw D3D12, then back up into a surviving frame result.

---

## The Destination

At the end of the path, the compute pass we want is just this:

In Unreal terms, this is the smallest believable render-graph-style compute pass: a texture output, a tiny parameter block, and one dispatch that clears it.

- one compute shader bytecode blob
- one UAV output texture
- one CBV carrying the clear color
- a root signature that maps those bindings into shader register space
- a compute PSO created against that root signature
- a command list that binds everything and calls `Dispatch(x, y, z)`
- barriers and fences that make the resource accesses legal

That model is intentionally small. It is enough to explain the D3D12 side without drifting into occupancy, wave ops, or algorithm design. The point is not to build an impressive effect. The point is to make one tiny pass survive the frame.

**Takeaway:** if you can trace this pass cleanly, bigger compute passes stop feeling mysterious. They become more of the same machinery.

---

## The Shader At The End Of The Path

To keep this concrete, use the smallest useful compute pass: clear a texture through a UAV.

```hlsl
RWTexture2D<float4> Output : register(u0);

cbuffer ClearParams : register(b0)
{
   float4 ClearColor;
};

[numthreads(8, 8, 1)]
void Main(uint3 dispatchThreadId : SV_DispatchThreadID)
{
   Output[dispatchThreadId.xy] = ClearColor;
}
```

It is intentionally boring. That is why it works.

- `RWTexture2D` makes the output a UAV-style object: writable, not sampled
- the constant buffer carries one small parameter block
- `[numthreads(8, 8, 1)]` defines the size of each thread group
- `Dispatch(x, y, z)` later decides how many groups to launch

There is almost no algorithm here. That is the point. Once the shader stops being interesting, the API work becomes impossible to ignore.

For this one shader to run in D3D12, the application still has to:

1. allocate the destination texture
2. create a UAV descriptor for it
3. create a CBV for the clear parameters
4. place those descriptors in a shader-visible heap
5. define a root signature that exposes `u0` and `b0`
6. create a compute PSO using the shader bytecode and that root signature
7. open a command list, bind everything, transition the texture to UAV state, and call `Dispatch`

That is the whole article in miniature. Nothing here is exotic. The difficulty is that every one of those steps has to line up before `Dispatch` stops being a line of code and becomes real GPU work.

**Takeaway:** the shader is not the lesson. The survival path around it is.

---

## The Path To Dispatch

The setup pipeline is easiest to understand as a dependency chain:

<div class="diagram-pipeline" style="margin:1.2em 0 1.4em;align-items:stretch;">
   <div class="dp-stage" style="border-color:var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);min-width:190px;">
      <div class="dp-title">1. Resources</div>
      <ul>
         <li>buffers</li>
         <li>textures</li>
         <li>upload or default heap memory</li>
      </ul>
   </div>
   <div class="dp-stage" style="border-color:var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);min-width:190px;">
      <div class="dp-title">2. Views</div>
      <ul>
         <li>SRV for reads</li>
         <li>UAV for writes</li>
         <li>CBV for constants</li>
      </ul>
   </div>
   <div class="dp-stage" style="border-color:var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);min-width:190px;">
      <div class="dp-title">3. Binding Space</div>
      <ul>
         <li>descriptor heap</li>
         <li>root signature</li>
         <li>compute PSO</li>
      </ul>
   </div>
   <div class="dp-stage" style="border-color:var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);min-width:220px;">
      <div class="dp-title">4. Recording</div>
      <ul>
         <li>allocator and command list reset</li>
         <li>`SetDescriptorHeaps` and `SetComputeRoot*`</li>
         <li>`Dispatch(x, y, z)`</li>
      </ul>
   </div>
   <div class="dp-stage" style="border-color:var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);min-width:220px;">
      <div class="dp-title">5. Submission</div>
      <ul>
         <li>`ExecuteCommandLists`</li>
         <li>queue signal</li>
         <li>fence wait or reuse check</li>
      </ul>
   </div>
   <div class="dp-stage" style="border-color:var(--color-neutral-300,#d4d4d4);background:var(--color-neutral-50,#fafafa);min-width:220px;">
      <div class="dp-title">6. Correctness</div>
      <ul>
         <li>resource state transitions</li>
         <li>UAV ordering barriers</li>
         <li>safe CPU-side lifetime reuse</li>
      </ul>
   </div>
</div>

<div style="font-size:.82em;opacity:.68;margin-top:-.7em;text-align:center;max-width:none;">
   Read it left to right: create memory, describe it, bind it, record the dispatch, submit it, then prove the accesses are legal.
</div>

This is the mental shift D3D12 forces. `Dispatch` stops being the story and becomes the last line in a longer chain.

{{< interactive-dispatch-ready >}}

Another way to frame it is by responsibility:

| Piece | What it answers |
| --- | --- |
| Resource + view | What memory is the shader allowed to see? |
| Descriptor heap | Where do those view descriptions live? |
| Root signature | How does shader register space map to bound data? |
| Compute PSO | Which shader and root signature define this dispatch? |
| Command list | In what order are bind and dispatch commands recorded? |
| Queue + fence | When does the GPU run this work, and when is it finished? |
| Resource barriers | Are the accesses legal for the states and hazards involved? |

That is the structure of the rest of the article. We are going to walk that path from left to right.

**Takeaway:** when a compute pass fails, debug the path, not just the kernel.

---

## Where This Dispatch Lives In The Frame

If you have read the frame graph articles, this should sound familiar: every pass lives in the same larger loop of **declare → compile → execute**. A compute pass is not a separate universe. It is one more frame step with explicit reads, writes, state transitions, and queue submission.

At a high level, a frame that contains compute usually looks like this:

<div class="diagram-steps" style="margin-top:1.1em;">
   <div class="ds-step">
      <div class="ds-num">1</div>
      <div>
         <strong>Frame begin:</strong> reset per-frame allocators, choose the descriptor versions for this frame, and prepare the resources the pass will touch.
      </div>
   </div>
   <div class="ds-step">
      <div class="ds-num">2</div>
      <div>
         <strong>Declare the compute pass:</strong> in frame-graph terms, this is where the pass says what it reads and writes. In raw D3D12, this same information exists implicitly in your chosen SRVs, UAVs, CBVs, and barriers.
      </div>
   </div>
   <div class="ds-step">
      <div class="ds-num">3</div>
      <div>
         <strong>Compile or prepare execution state:</strong> the engine decides ordering, queue placement, and transitions. In a frame graph, that is the compile stage. In bare D3D12, you record the equivalent choices manually.
      </div>
   </div>
   <div class="ds-step">
      <div class="ds-num">4</div>
      <div>
         <strong>Record the compute commands:</strong> set heaps, set the compute root signature, set the PSO, bind descriptor tables or root views, transition resources, then call <code>Dispatch</code>.
      </div>
   </div>
   <div class="ds-step">
      <div class="ds-num">5</div>
      <div>
         <strong>Hand the result back to the frame:</strong> transition the output back into whatever the next pass needs, whether that is another compute step, a graphics pass, or presentation much later in the frame.
      </div>
   </div>
   <div class="ds-step">
      <div class="ds-num">6</div>
      <div>
         <strong>Frame end:</strong> fences tell the CPU when it is safe to reuse allocator memory, upload memory, and descriptor heap space for the next frame.
      </div>
   </div>
</div>

That is the relationship to the frame graph series. Those articles describe the renderer-level scheduling problem. This article zooms all the way in to what one compute pass looks like at the API boundary.

Put differently: the frame graph says <em>when</em> a compute pass can run and what it depends on. This article says what that same pass looks like when it finally turns into D3D12 commands.

For Unreal readers, this is the important shift: a render graph pass is not just a place to put the dispatch. It is the frame-level context that decides whether the dispatch survives contact with the rest of the frame.

**Takeaway:** the pass is only half the story. The frame around it decides whether the result survives.

---

## Why This Is Not Just "A Draw Call, But Compute"

The easiest way to get lost in D3D12 compute is to think of it as "the graphics pipeline, but with different shaders." That framing breaks almost immediately.

Both graphics and compute use command lists, root signatures, descriptor heaps, PSOs, barriers, and queues. The difference is in what the pipeline expects to be bound before work is legal.

<div class="diagram-ftable">
<table>
   <tr><th>Question</th><th>Graphics pass</th><th>Compute pass</th></tr>
   <tr><td><strong>Main execution call</strong></td><td><code>Draw*</code></td><td><code>Dispatch</code></td></tr>
   <tr><td><strong>Pipeline object</strong></td><td>Graphics PSO</td><td>Compute PSO</td></tr>
   <tr><td><strong>Root binding entrypoints</strong></td><td><code>SetGraphicsRoot*</code></td><td><code>SetComputeRoot*</code></td></tr>
   <tr><td><strong>Fixed-function setup</strong></td><td>Input assembly, rasterization, render-target or depth output</td><td>None of that path is active</td></tr>
   <tr><td><strong>Typical outputs</strong></td><td>RTV or DSV writes</td><td>UAV writes</td></tr>
   <tr><td><strong>Typical data model</strong></td><td>Vertices, indices, render targets, viewport state</td><td>SRV/UAV/CBV resources plus thread-group dimensions</td></tr>
   <tr><td><strong>Common barrier concern</strong></td><td>RTV/DSV/SRV transitions between passes</td><td>SRV/UAV transitions plus UAV ordering hazards</td></tr>
</table>
</div>

That is why the tiny clear-texture example matters. It strips compute down to its real essentials:

- no vertex input
- no render targets
- no viewport or scissor setup
- no raster stage at all
- just resources, bindings, a compute PSO, and `Dispatch`

That is also why compute is such a natural fit for passes like clears, copies, prefix sums, culling, tiled-light list construction, denoisers, bloom, and particle simulation. They are resource-processing problems, not triangle-processing problems.

**Takeaway:** if the job is really "take resources in, write resources out," compute is the natural abstraction. The low-level cost is that you have to make every resource interaction explicit.

---

## Step 1: Declare The Binding Contract

The root signature is the first boundary that really matters. It defines the binding space the command list has to populate before draw or dispatch. In compute, shader visibility is conceptually simpler than graphics because there is only one active programmable stage. The practical effect is that compute bindings flow through the `SetComputeRoot*` family of calls.

If you are coming from Unreal, this is the lower-level version of the binding contract the engine usually lets you express through shader parameters and pass setup.

At a high level, the root signature can contain three kinds of things:

- descriptor tables, which point into descriptor heaps
- root descriptors, which place a small descriptor directly in the root arguments
- root constants, which place 32-bit values directly in the root arguments

For this tiny clear path, descriptor tables are the simplest useful choice because they map directly to the UAV and CBV descriptors the shader needs.

```cpp
CD3DX12_DESCRIPTOR_RANGE1 ranges[2];
ranges[0].Init(D3D12_DESCRIPTOR_RANGE_TYPE_UAV, 1, 0);
ranges[1].Init(D3D12_DESCRIPTOR_RANGE_TYPE_CBV, 1, 0);

CD3DX12_ROOT_PARAMETER1 params[2];
params[0].InitAsDescriptorTable(1, &ranges[0]);
params[1].InitAsDescriptorTable(1, &ranges[1]);

CD3DX12_VERSIONED_ROOT_SIGNATURE_DESC rootSigDesc;
rootSigDesc.Init_1_1(_countof(params), params, 0, nullptr);
```

That snippet expresses the core architectural idea: the shader does not see raw resources directly. It sees register bindings, and the root signature explains how runtime bindings satisfy them.

There are two practical constraints worth calling out early.

First, samplers live in a separate descriptor heap type. A descriptor table cannot mix samplers with CBV, SRV, and UAV descriptors.

Second, the root signature and the pipeline state must match by the time `Dispatch` happens. Setting a PSO does not automatically change the root signature, and setting a root signature does not automatically change the PSO. That separation is powerful, but it is also one of the easiest ways to make a command list invalid.

This is a good place to make the reader do the mapping directly instead of only reading the sample. If they cannot match the shader bindings to real root parameters, they do not really own the concept yet.

**Takeaway:** before the GPU can read your parameter struct, D3D12 needs a root signature that says exactly where every binding lives.

{{< interactive-root-binding >}}

---

## Step 2: Describe The Data

The texture exists now, but the shader still cannot see it. That changes only once the GPU gets views that describe what that texture means.

In Unreal terms, this is the part that usually feels like "I have a texture and I exposed it to the pass." At the D3D12 layer, that friendly step expands into concrete UAV and CBV descriptions.

For this clear example, the important cases are simple:

- UAV for writable output or read/write access
- CBV for small parameter blocks

The API reflects that split directly with `CreateUnorderedAccessView` and `CreateConstantBufferView`.

```cpp
D3D12_UNORDERED_ACCESS_VIEW_DESC uavDesc = {};
uavDesc.Format = DXGI_FORMAT_R16G16B16A16_FLOAT;
uavDesc.ViewDimension = D3D12_UAV_DIMENSION_TEXTURE2D;

D3D12_CONSTANT_BUFFER_VIEW_DESC cbvDesc = {};
cbvDesc.BufferLocation = constantBuffer->GetGPUVirtualAddress();
cbvDesc.SizeInBytes = (sizeof(Constants) + 255) & ~255;
```

Two details matter immediately.

First, the UAV is not "the texture." It is the view that tells the GPU to treat that texture as a writable `Texture2D`-style resource for the shader.

Second, the CBV size must be 256-byte aligned.

Those descriptors then live in descriptor heaps. For shader-visible compute binding, the relevant heap type is the combined `CBV_SRV_UAV` heap. D3D12 allows at most one bound heap of that type and at most one sampler heap at a time, and those heaps are shared by both graphics and compute binding state.

That matters more than it first appears. Descriptor heap changes are not just local housekeeping. On some hardware, switching heaps is expensive enough that the practical pressure is obvious: treat heap switching as a coarse event and root descriptor table updates as the fine-grained operation.

The second pressure is lifetime. A descriptor heap location cannot be modified while submitted GPU work may still reference it. This is one of the recurring D3D12 themes: the application, not the driver, owns the versioning problem.

At this point we finally have something the shader could consume. We still do not have a pipeline that can run it.

**Takeaway:** "I have a texture" is not enough. The shader sees views, not raw engine objects.

---

## Step 3: Freeze The Pipeline

Once the root signature exists and shader bytecode has been compiled, the next immutable object is the compute PSO.

Conceptually, `CreateComputePipelineState` freezes two things into one object:

- the compute shader bytecode
- the root signature it is expected to run with

```cpp
D3D12_COMPUTE_PIPELINE_STATE_DESC psoDesc = {};
psoDesc.pRootSignature = rootSignature.Get();
psoDesc.CS = { csBlob->GetBufferPointer(), csBlob->GetBufferSize() };

ComPtr<ID3D12PipelineState> computePso;
ThrowIfFailed(device->CreateComputePipelineState(
    &psoDesc,
    IID_PPV_ARGS(&computePso)));
```

The important part is that the PSO is immutable. The command list selects an already-created PSO. It does not mutate a live pipeline object in place.

That is why the pairing with the root signature matters so much. D3D12 wants compatibility to be explicit at creation time and stable at execution time.

Now the pass has a shader contract and a pipeline object. It still is not work. For that, we need a command list.

From an Unreal point of view, this is one of the places where the engine hides a lot for you. You think "dispatch this shader." D3D12 thinks in terms of immutable pipeline state and compatibility.

**Takeaway:** by the time the pass is recorded, shader choice and binding compatibility need to already be frozen into a compute PSO.

---

## Step 4: Record The Work

At this point the objects exist. Now the question is narrower: what exact sequence turns them into GPU work?

This is the closest point to the usual Unreal mental model of "the pass actually runs here." The difference is that D3D12 makes the recording sequence fully explicit.

For the clear-texture example, the command list follows this shape:

```cpp
ThrowIfFailed(allocator->Reset());
ThrowIfFailed(cmd->Reset(allocator.Get(), computePso.Get()));

cmd->ResourceBarrier(1, &CD3DX12_RESOURCE_BARRIER::Transition(
   outputTexture.Get(),
   D3D12_RESOURCE_STATE_COMMON,
    D3D12_RESOURCE_STATE_UNORDERED_ACCESS));

ID3D12DescriptorHeap* heaps[] = { cbvSrvUavHeap.Get() };
cmd->SetDescriptorHeaps(_countof(heaps), heaps);
cmd->SetComputeRootSignature(rootSignature.Get());
cmd->SetPipelineState(computePso.Get());

cmd->SetComputeRootDescriptorTable(0, outputUavHandle);
cmd->SetComputeRootDescriptorTable(1, constantsCbvHandle);

cmd->Dispatch((width + 7) / 8, (height + 7) / 8, 1);

cmd->ResourceBarrier(1, &CD3DX12_RESOURCE_BARRIER::Transition(
   outputTexture.Get(),
    D3D12_RESOURCE_STATE_UNORDERED_ACCESS,
    D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE));

ThrowIfFailed(cmd->Close());
```

There are several D3D12 ideas packed into that small sequence.

The command allocator and command list are separate objects. The allocator owns memory used for recorded commands; the list owns the logical recording stream.

Reset rules are asymmetric. A command list can be reset aggressively, but an allocator cannot be reset until the GPU has finished executing all command lists that depend on it. That is why fences matter even for a single-queue setup.

`Dispatch` itself is simple in signature, but it is not doing any hidden setup for you. The call only works because every requirement earlier in the chain has already been satisfied. The per-dimension dispatch counts are also bounded: the D3D12 `Dispatch` documentation caps each dimension at 65535, with feature-level-specific constraints on `Z` for lower feature levels.

This is also where readers usually benefit from one forced translation step: given a pass description, can they actually name the states the resources need before and after the dispatch?

**Takeaway:** recording is where all the earlier setup either snaps together cleanly or falls apart.

{{< interactive-compute-states >}}

---

## Step 5: Submit The Work

Recording commands is still not execution. D3D12 execution happens when a command queue consumes closed command lists.

```cpp
ID3D12CommandList* lists[] = { cmd.Get() };
queue->ExecuteCommandLists(_countof(lists), lists);

const UINT64 signalValue = ++fenceValue;
ThrowIfFailed(queue->Signal(fence.Get(), signalValue));

if (fence->GetCompletedValue() < signalValue)
{
    ThrowIfFailed(fence->SetEventOnCompletion(signalValue, fenceEvent));
    WaitForSingleObject(fenceEvent, INFINITE);
}
```

This is the point where D3D12's ownership model stops being theoretical.

The queue owns execution order. The fence is the API-visible progress marker that tells the CPU which submitted unit of work has completed. Without that fence, the application does not know when it is safe to reuse allocators, overwrite upload memory, or recycle descriptor heap regions that might still be referenced by the GPU.

The same model scales to multiple queues as well. The official queue documentation makes the ownership rule clear: a resource cannot be written from multiple command queues simultaneously, and once a queue has a resource in a writable state, that queue effectively owns it until the resource transitions back to a read or common state.

Even if this article stays on one queue, that rule matters now because it explains why "compute queue later" is a synchronization topic, not just a scheduling topic.

At this point the dispatch is real. It has been recorded and submitted. One piece is still missing: proving the memory accesses mean what we think they mean.

This is another place where engine users benefit from seeing the lower layer once. Queue submission and fence ownership are usually far away from day-to-day pass authoring, but they are still part of the path your pass takes.

**Takeaway:** a recorded dispatch is still not work. It only becomes real once a queue executes it and the engine tracks ownership correctly.

---

## Step 6: Make It Legal

If you only remember one correctness rule from this article, it should be this: a transition barrier and a UAV barrier solve different hazards.

A transition barrier changes the declared usage state of a resource. That is what you use when a buffer or texture moves between states such as shader-readable and unordered-access.

A UAV barrier is about ordering UAV accesses. It tells D3D12 that earlier UAV reads or writes relevant to that barrier must complete before later UAV accesses begin.

That distinction matters because "resource is in `UNORDERED_ACCESS`" is not the same statement as "all prior UAV writes are visible in the way my next dispatch expects."

The official D3D12 barrier documentation also makes two practical points that are easy to miss:

- you do not need a UAV barrier between dispatches that only read from a UAV
- you also do not need one between writes if the application genuinely does not care about ordering between those writes

That means UAV barriers are not "always after every dispatch." They are correctness tools for specific ordering requirements.

This is where the scope needs discipline. Part I should explain what the barrier means at the API level and when it is needed. It should not turn into a general memory-model article.

This is a good place for a small interactive because the rule is easy to say and easy to misremember. The point is not to gamify barriers. It is to make the difference between "same state" and "correct ordering" tangible.

**Takeaway:** surviving the frame means more than "the shader ran." It means the next pass sees the result in the state and order you intended.

{{< interactive-uav-barrier >}}

---

## What Was Hiding Behind One Dispatch

By this point the common failure modes are predictable. The docs are explicit about them. The hard part is that the API will happily let you assemble the problem one step at a time.

### 1. Root signature and PSO drift apart

The root signature bound at dispatch time must be compatible with the active PSO. D3D12 does not paper over that mismatch for you.

### 2. Descriptor heap contents are treated like ordinary CPU memory

They are CPU-managed, but shader-visible descriptor locations still have GPU lifetime constraints. If submitted work may read a location, that location is not yours to overwrite yet.

### 3. Allocators are reset too early

Allocator reset is gated by GPU completion, not by "I already called `ExecuteCommandLists`."

### 4. Resource state is handled, but UAV ordering is ignored

A resource can be in the right state and still require a UAV barrier between dependent read/write phases.

### 5. Dispatch is treated like the beginning of the compute story

In D3D12, `Dispatch` is the end of the setup story. Most of the actual API design happens before it.

If you are reading this from an Unreal mindset, that last point is the one worth keeping. The friendly pass authoring view is real, but underneath it the low-level path is still there, and that path is exactly where failure cases come from.

**Takeaway:** the pass disappears for concrete reasons. Root mismatch, descriptor lifetime, allocator reuse, wrong state, missing ordering. That is a debuggable list, not a mystery.

---

## What This Article Is Not

There are a few adjacent topics that are real, useful, and deliberately out of scope for Part I:

- bindless-style indexing strategies across large descriptor spaces
- bundle-specific compute recording patterns
- split barriers and multi-engine overlap tuning
- detailed Root Signature 1.1 static-ness promises as a performance topic
- Vulkan mapping details such as descriptor sets, pipeline layouts, and queue family ownership

Those are good follow-up subjects. They are not necessary to explain the first legal, understandable compute path in D3D12.

---

## The Payoff

Once you look at compute through the D3D12 API instead of through shader code, the shape of the problem changes.

The dispatch itself is tiny. The system around it is not. The real work is declaring the binding contract, describing the data, freezing the pipeline, recording the right command sequence, and synchronizing memory so the GPU sees exactly the accesses you intended.

That sounds like extra ceremony because it is extra ceremony. But it is also why D3D12 compute stays tractable at scale: the model is explicit enough that engines can reason about it, cache it, batch it, validate it, and eventually feed it into larger scheduling systems.

That is the value of looking at the path instead of only looking at the shader. Once you see what has to line up for one tiny clear pass, the rest of D3D12 compute stops feeling like opaque ceremony and starts feeling like explicit machinery.

This article stays deliberately on the D3D12 side of that boundary. One legal pass. One explicit chain. Part II can take that same chain and map it onto Vulkan one object at a time.

If the article does its job, the takeaway should be simple:

- you can now trace a tiny Unreal-style compute clear pass all the way down to D3D12
- you know which objects must exist before `Dispatch` is legal
- you have a better debugging model for "the pass did not survive the frame"
- you have the right mental unit for bigger topics that come later

---

## References

Primary public sources used for this draft:

1. Microsoft Learn, Creating a Root Signature
   https://learn.microsoft.com/en-us/windows/win32/direct3d12/creating-a-root-signature
2. Microsoft Learn, Descriptor Heaps Overview
   https://learn.microsoft.com/en-us/windows/win32/direct3d12/descriptor-heaps-overview
3. Microsoft Learn, Creating Descriptors
   https://learn.microsoft.com/en-us/windows/win32/direct3d12/creating-descriptors
4. Microsoft Learn, Creating and recording command lists and bundles
   https://learn.microsoft.com/en-us/windows/win32/direct3d12/recording-command-lists-and-bundles
5. Microsoft Learn, Executing and Synchronizing Command Lists
   https://learn.microsoft.com/en-us/windows/win32/direct3d12/executing-and-synchronizing-command-lists
6. Microsoft Learn, Using Resource Barriers to Synchronize Resource States in Direct3D 12
   https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12
7. Microsoft Learn, ID3D12Device::CreateComputePipelineState
   https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-createcomputepipelinestate
8. Microsoft Learn, ID3D12GraphicsCommandList::Dispatch
   https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-dispatch
9. Microsoft Learn, HLSL `RWTexture2D`
   https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-object-rwtexture2d
10. DirectX-Specs, D3D12 Resource Binding Functional Spec
   https://microsoft.github.io/DirectX-Specs/d3d/ResourceBinding.html