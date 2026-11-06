# diverse-opinions

An agent skill that gets a wide spread of opinions on one question. It runs one fresh subagent per persona, where each persona is a different randomly sampled ordinary person, and then merges the answers into distinct positions without averaging them.

## Why

A single model answering the same question many times keeps landing on the same answers. The paper "A Cognitive Framework for Idea Diversity in Large Language Models" (Deng, Brucks and Toubia, arXiv 2602.20408) names two causes. Every session starts in the same region of ideas, and inside one session the first ideas anchor the rest. This skill applies the paper's two fixes: a different random persona per session, and a short-titles-first, then bolder, then expand routine inside each session.

The paper tested product ideas. This skill applies the same procedure to opinions, which the paper did not test, so the output prompts thinking and is not evidence about what real people believe.

## Install

Copy `SKILL.md` and the `scripts` folder into a skill folder named `diverse-opinions`, for example:

```bash
git clone https://github.com/wanderingspirit03/diverse-opinions ~/.agents/skills/diverse-opinions
```

The skill file calls `python3 ~/.agents/skills/diverse-opinions/scripts/sample_personas.py`, so change that path in `SKILL.md` if you install somewhere else. It needs an agent that can run subagents in parallel (for example Claude Code).

## Personas and licensing

Personas come from [PersonaHub](https://huggingface.co/datasets/proj-persona/PersonaHub) (200,000 synthetic people). This repository does not contain the dataset. On first use the script downloads about 21.6 MB into `~/.cache/diverse-opinions/`. The dataset is licensed CC BY-NC-SA 4.0, so do not copy it into a product or repository. If the download fails, the script exits with status 2 and the skill tells the agent to write personas itself, which gives less spread.

## Use

Ask your agent for several different views on a question, for example "give me 8 different takes on whether to open source this". Use `--seed` to repeat a run:

```bash
python3 scripts/sample_personas.py --n 8 --seed 123
```

## License

The skill file and script are MIT licensed. The PersonaHub dataset keeps its own license.
