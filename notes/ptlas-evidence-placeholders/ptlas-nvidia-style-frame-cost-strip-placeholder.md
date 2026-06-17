# PTLAS NVIDIA-Style Frame-Cost Strip Placeholder

Status: capture needed

Purpose:

- show acceleration-structure update cost as one part of the frame
- avoid presenting PTLAS as a feature win without timing context

Frame-cost fields:

| Frame cost field | Classic TLAS | PTLAS | Source |
|---|---:|---:|---|
| physics time | capture needed | capture needed | capture needed |
| update record generation time | capture needed | capture needed | capture needed |
| TLAS update time | capture needed | not applicable | capture needed |
| PTLAS update time | not applicable | capture needed | capture needed |
| render time | capture needed | capture needed | capture needed |
| changed-instance count | capture needed | capture needed | capture needed |
| touched-partition count | not applicable | capture needed | capture needed |
| native operation type/count | capture needed | capture needed | capture needed |
| memory | capture needed | capture needed | capture needed |
| scratch | capture needed | capture needed | capture needed |

Visual design notes:

- horizontal strip or stacked timing bars
- acceleration-structure update should be visible beside other frame work
- timing bars must not be drawn until values are captured
