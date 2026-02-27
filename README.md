# SSI Generative AI Risk Register

A community-maintained register of risks associated with the use of AI in 
Research Software Engineering, maintained by the SSI Responsible AI Study Group.

## What is this?

This register has been developed by the Software Sustainability Institute's Responsible AI in RSE study group for Collaboration Workshop 2026. It is designed to encourage continual contribution from the RSE community, and allow them to identify the AI risks that are most pertinent to them. As the AI landscape continues to evolve, it is crucial that we develop guidelines which are relevant, adaptable, and actionable. This risk register will allow us to achieve that.

## Scope

This register is intended to capture concerns around the use of generative AI in the development of research software. While there are valid concerns around the use of AI more generally as an analytic tool, or of generative AI in other areas of science, these are best addressed through discussion with the wider academic community.

Risks need not be applicable to all RSEs in all fields. If there are risks that are specific to your work then please include them — you may be surprised how relevant they are to others!

## How to Contribute

Details of how to contribute are in [CONTRIBUTING.md](CONTRIBUTING.md). Contributions can be made with or without a GitHub account.

To propose a new risk, go to the "Issues" tab and select "New issue" and "Propose new risk". See below for detailed information about each field. If you don't have a GitHub account, then a risk can be added manually using this [Microsoft form](#).

If you would like to be recognised as a contributor to the register, please add your name to [CONTRIBUTORS.md](CONTRIBUTORS.md) via a pull request.

## The Register

The live register is found in [/register/risks.csv](/register/risks.csv).

### Fields

The register has six editable fields. Please be as descriptive as possible when filling in the fields. An explanation of each field is given below.

**Risk**: A description of the nature of the risk — who does it affect? What are the potential outcomes?

**Likelihood**: Choice of *Low*, *Medium*, *High*, or *Unknown*.

* *Low* -- Unlikely to occur in normal RSE practice, even in the long term.
* *Medium* -- Plausible and has been observed in similar contexts, or likely to be an issue in the near future.
* *High* -- Commonly encountered or well-documented. A current and existing issue.
* *Unknown* -- Evidence is lacking or highly contested.

**Severity**: Choice of *Low*, *Medium*, *High*, or *Unknown*.

* *Low* -- Minor inconvenience or easily remedied. Limited impact on research outputs or individuals.
* *Medium* -- Meaningful impact on research quality, professional practice, or individuals. Recoverable but non-trivial.
* *High* -- Significant harm to research integrity, individuals, or communities. Potentially irreversible.
* *Unknown* -- Severity is highly context-dependent or insufficient evidence exists to assess.

**Mitigations**: (Optional) Any potential ways in which the risk might be mitigated, either through changing RSE practice, institutional policy, or other means.

**Ownership**: (Optional) Who is responsible for addressing this risk? This might be practitioners, institutions, funders, government, or tool developers. It might be multiple people or groups.

**Examples**: (Optional) Are there any examples of where this risk has been managed elsewhere? Please provide any relevant links or evidence if available.

**Issue**: (Not editable) A unique identifier for the risk, which can be used to reference it when submitting updates.

## Governance

The register is maintained by the SSI's Responsible AI in RSE study group. All edits to the register (e.g., new risks, updates to existing risks) are reviewed by the study group. The register is periodically reviewed to merge similar risks and remove redundancy.

## Data Usage and Confidentiality

Contributions to this register are made publicly under CC BY 4.0 and may be used in future research. No personally identifying information should be included in contributions.

## Citation

Please cite as:

```text
@misc{ssi_ai_risk_register_2026,
  author       = {Shingleton, Joseph and {SSI Responsible AI Study Group}},
  title        = {{SSI Generative AI Risk Register}},
  year         = {2026},
  publisher    = {Software Sustainability Institute},
  howpublished = {\url{https://github.com/jshng-glasgow/SSI-Responsbile-AI-Risk-Register/}}
}
```