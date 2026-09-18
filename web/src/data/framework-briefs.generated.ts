/**
 * GENERATED FILE. Do not edit by hand.
 * Source: docs/frameworks/*.md
 * Regenerate with: bun run briefs
 */

import type { Framework } from "../lib/types";

export type Run = { text: string; strong?: boolean; em?: boolean };
export type ListItem = { label?: Run[]; runs: Run[]; children?: ListItem[] };
export type Block =
  | { kind: "p"; runs: Run[] }
  | { kind: "ul"; items: ListItem[] }
  | { kind: "ol"; items: ListItem[] }
  | { kind: "table"; head: Run[][]; rows: Run[][][] }
  | { kind: "group"; heading: string; blocks: Block[] };
export type BriefSection = { heading: string; blocks: Block[] };
export type FrameworkBrief = {
  id: Framework;
  fullName: string;
  origin: string | null;
  why: Block[];
  sections: BriefSection[];
};

export const FRAMEWORK_BRIEFS: Record<Framework, FrameworkBrief> = {
  "STAR": {
    "id": "STAR",
    "fullName": "Situation, Task, Action, Result",
    "origin": "Developed in organizational psychology (Dr. Tom Janz, DDI) and standardized across tier-1 technology firms (Amazon Leadership Principles, Google Structured Interviews). Grounded in the behavioral axiom that structured past performance under constraints is the single highest predictor of future execution.",
    "why": [
      {
        "kind": "ul",
        "items": [
          {
            "label": [
              {
                "text": "Core Philosophy"
              }
            ],
            "runs": [
              {
                "text": "Rather than allowing candidates to recite abstract platitudes or theoretical beliefs (\"I'm a great team player who loves clean code\"), STAR forces the candidate to reconstruct a factual narrative arc: "
              },
              {
                "text": "Context → Responsibility → Execution → Impact",
                "strong": true
              },
              {
                "text": "."
              }
            ]
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "STAR Sentence Stems & Language Patterns",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Component"
                }
              ],
              [
                {
                  "text": "Strong Sentence Stems"
                }
              ],
              [
                {
                  "text": "Anti-Pattern Phrases to Avoid"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "Situation",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"At [Company/Project], our core service was handling [Volume/Context] when [Trigger Event occurred]...\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"In my opinion, backend systems should always...\"",
                    "em": true
                  },
                  {
                    "text": " (Hypothetical)"
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Task",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"My specific responsibility as the tech lead was to [Objective] without [Constraint/Downtime]...\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"We had a bunch of random tasks to do.\"",
                    "em": true
                  },
                  {
                    "text": " (Vague)"
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Action",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"I approached this in three phases: first, I diagnosed [X]; second, I designed [Y]; and third, I collaborated with [Team] to [Z]...\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"We just got together and somehow fixed it.\"",
                    "em": true
                  },
                  {
                    "text": " (Passive \"We\")"
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Result",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Quantitative:",
                    "em": true
                  },
                  {
                    "text": " "
                  },
                  {
                    "text": "\"This brought our downtime from 4 hours to zero...\"",
                    "em": true
                  },
                  {
                    "text": "<br>"
                  },
                  {
                    "text": "Operational:",
                    "em": true
                  },
                  {
                    "text": " "
                  },
                  {
                    "text": "\"This unblocked the release gate and established our standard deployment playbook...\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"Everything was fine in the end.\"",
                    "em": true
                  },
                  {
                    "text": " (No identifiable impact)"
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Key Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: Authentic Situational Grounding (Without Academic Pedantry)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "What We Look For"
                      }
                    ],
                    "runs": [
                      {
                        "text": "The candidate anchors the narrative in an authentic, past context (identifying a project, system, client, team, or operating constraint)."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Realistic Balance"
                      }
                    ],
                    "runs": [
                      {
                        "text": "We do "
                      },
                      {
                        "text": "not",
                        "strong": true
                      },
                      {
                        "text": " require exhaustive company histories, audited financials, or legal citations. A simple, credible anchor ("
                      },
                      {
                        "text": "\"Last year on our payment gateway service...\", \"During our cloud migration at...\"",
                        "em": true
                      },
                      {
                        "text": ") is completely sufficient."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "What to Penalize"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Speaking entirely in abstract, hypothetical generalities ("
                      },
                      {
                        "text": "\"Whenever I build an API, you should always write tests...\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Balanced Personal Agency (Owning Contribution While Respecting Team)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "What We Look For"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Isolating what the "
                      },
                      {
                        "text": "candidate",
                        "em": true
                      },
                      {
                        "text": " specifically did. Interviewers cannot hire a team; they hire the individual."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Realistic Balance"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Healthy candidates naturally collaborate and acknowledge teammates ("
                      },
                      {
                        "text": "\"Our team had to hit a tight deadline, so I took ownership of the caching layer...\"",
                        "em": true
                      },
                      {
                        "text": "). This is "
                      },
                      {
                        "text": "positive",
                        "strong": true
                      },
                      {
                        "text": " and should not be penalized."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "What to Penalize"
                      }
                    ],
                    "runs": [
                      {
                        "text": "The passive, hiding \"we\" where individual contribution is invisible ("
                      },
                      {
                        "text": "\"We decided to rewrite everything and then we tested it and we shipped it\"",
                        "em": true
                      },
                      {
                        "text": "—leaving the listener with zero clue what the candidate actually did)."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Impact is Mandatory — But Numbers Are NOT the Only Valid Impact",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Critical Distinction"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Not every meaningful engineering or leadership contribution produces a tidy decimal percentage or revenue statistic. Forcing artificial numbers leads to hallucinated or disingenuous answers."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Two Equally Valid Forms of Impact"
                      }
                    ],
                    "runs": [],
                    "children": [
                      {
                        "label": [
                          {
                            "text": "Quantitative Metrics"
                          }
                        ],
                        "runs": [
                          {
                            "text": "Measurable numbers, percentages, latency reductions, cost savings, hours recovered (e.g., "
                          },
                          {
                            "text": "\"reduced P99 latency by 45%\", \"saved ₦10M annually\", \"increased throughput to 15k RPS\"",
                            "em": true
                          },
                          {
                            "text": ")."
                          }
                        ]
                      },
                      {
                        "label": [
                          {
                            "text": "Qualitative / Operational / Strategic Impact"
                          }
                        ],
                        "runs": [
                          {
                            "text": "Tangible, observable differences made to the team, architecture, or organization even without numbers (e.g., "
                          },
                          {
                            "text": "\"unblocked the mobile team so they met the App Store release deadline\", \"prevented customer churn by resolving a contract deadlock with an enterprise client\", \"established an architectural pattern that was adopted across 3 other services\", \"eliminated a dangerous single point of failure\"",
                            "em": true
                          },
                          {
                            "text": ")."
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "What to Penalize"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Complete absence of impact, unresolved cliffhangers ("
                      },
                      {
                        "text": "\"and then we just worked on other things\"",
                        "em": true
                      },
                      {
                        "text": "), or meaningless filler ("
                      },
                      {
                        "text": "\"it went fine\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Pacing & Structural Discipline",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Target Pacing Ratio"
                      }
                    ],
                    "runs": [],
                    "children": [
                      {
                        "label": [
                          {
                            "text": "Situation (~15%)"
                          }
                        ],
                        "runs": [
                          {
                            "text": "Crisp setup; 2–3 sentences."
                          }
                        ]
                      },
                      {
                        "label": [
                          {
                            "text": "Task (~15%)"
                          }
                        ],
                        "runs": [
                          {
                            "text": "Clearly isolating the core problem or mission."
                          }
                        ]
                      },
                      {
                        "label": [
                          {
                            "text": "Action (~55%)"
                          }
                        ],
                        "runs": [
                          {
                            "text": "The meat of the answer—decisions, tools, trade-offs, obstacles overcome."
                          }
                        ]
                      },
                      {
                        "label": [
                          {
                            "text": "Result (~15%)"
                          }
                        ],
                        "runs": [
                          {
                            "text": "The punchline—tangible impact, deliverables, or lessons."
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Failure Mode (The History Lecture)"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Spending 70 seconds on background lore and only having 20 seconds left to rush through what was actually done."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "CARL": {
    "id": "CARL",
    "fullName": "Context, Action, Result, Learning",
    "origin": null,
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "While the "
          },
          {
            "text": "STAR",
            "strong": true
          },
          {
            "text": " framework evaluates past execution and task delivery, senior and leadership roles demand an even more critical capability: "
          },
          {
            "text": "metacognition, intellectual humility, and systemic learning",
            "strong": true
          },
          {
            "text": "."
          }
        ]
      },
      {
        "kind": "p",
        "runs": [
          {
            "text": "The "
          },
          {
            "text": "CARL Framework",
            "strong": true
          },
          {
            "text": " ("
          },
          {
            "text": "Context, Action, Result, Learning",
            "strong": true
          },
          {
            "text": ") is the executive standard for evaluating how a professional handles failures, unexpected pivots, architectural trade-offs, and organizational growth. In tier-1 engineering and leadership assessments (Senior, Staff, Principal, Director), interviewers specifically listen to the "
          },
          {
            "text": "Learning",
            "strong": true
          },
          {
            "text": " phase to determine whether a candidate has 10 years of evolving experience or simply 1 year of experience repeated 10 times."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "Key Differences Between STAR and CARL",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Dimension"
                }
              ],
              [
                {
                  "text": "STAR (Situation, Task, Action, Result)"
                }
              ],
              [
                {
                  "text": "CARL (Context, Action, Result, Learning)"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "Primary Focus",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Task completion, problem solving, individual agency."
                  }
                ],
                [
                  {
                    "text": "Metacognition, failure recovery, systemic resilience."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Target Seniority",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Mid-level, Senior Engineer, Individual Contributor."
                  }
                ],
                [
                  {
                    "text": "Senior, Staff, Principal, Engineering Manager, Director."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Narrative Climax",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "The "
                  },
                  {
                    "text": "Result",
                    "strong": true
                  },
                  {
                    "text": " (the deliverable, metric, or resolution)."
                  }
                ],
                [
                  {
                    "text": "The "
                  },
                  {
                    "text": "Learning",
                    "strong": true
                  },
                  {
                    "text": " (the shift in mental models and permanent safeguards)."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Ideal Prompt Types",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"Tell me about a time you shipped a hard project.\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"Tell me about a time an assumption you made was wrong.\"",
                    "em": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Time Allocation",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "15% S, 15% T, 55% A, 15% R"
                  }
                ],
                [
                  {
                    "text": "15–20% C, 35% A, 15% R, "
                  },
                  {
                    "text": "25–30% L",
                    "strong": true
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Core Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: The \"Learning\" is the True Climax",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In STAR, once the Result is shared, the story concludes."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "In CARL, the Result is merely the setup for the most important phase: "
                      },
                      {
                        "text": "the Learning",
                        "strong": true
                      },
                      {
                        "text": ". If a speaker spends 90 seconds detailing technical actions and concludes with a 5-second generic quip ("
                      },
                      {
                        "text": "\"And so I learned to always test my code\"",
                        "em": true
                      },
                      {
                        "text": "), the answer is an "
                      },
                      {
                        "text": "incomplete failure",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "The Learning must account for "
                      },
                      {
                        "text": "25% to 30%",
                        "strong": true
                      },
                      {
                        "text": " of the answer's duration and depth."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Systemic Learning vs. Superficial Platitudes",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Weak (Superficial Platitude)"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"I learned that communication is really important across teams.\"",
                        "em": true
                      },
                      {
                        "text": " (Tells the interviewer nothing about technical depth or executive maturity)."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Strong (Systemic Safeguards)"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"That incident showed me that our staging environment completely masked lock contention because synthetic data lacked real-world skew. As a result, I permanently altered our engineering playbook: we instituted automated chaos runs with production-cloned distributions, and I created a post-mortem review template now used across all four squads.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Authentic Humility Over Defensive Externalization",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In failure, outage, or pivot prompts, interviewers explicitly test for "
                      },
                      {
                        "text": "defensive externalization",
                        "strong": true
                      },
                      {
                        "text": " (blaming management, legacy code, juniors, or shifting deadlines)."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Candidates who openly own their misjudgments ("
                      },
                      {
                        "text": "\"My assumption at the time was X, which was flawed because I overlooked Y\"",
                        "em": true
                      },
                      {
                        "text": ") demonstrate emotional maturity and psychological safety."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Balanced Result & Impact (Quantitative & Operational)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "As established in our core philosophy, results do "
                      },
                      {
                        "text": "not",
                        "strong": true
                      },
                      {
                        "text": " need to be solely numeric percentages."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Valid Quantitative Results"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"We recovered database throughput within 45 minutes, limiting downtime to 0.02%.\"",
                        "em": true
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Valid Qualitative/Operational Results"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"We unblocked the mobile release branch, re-established trust with our enterprise banking partner, and eliminated a high-risk architectural single-point-of-failure.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "PAR": {
    "id": "PAR",
    "fullName": "Problem, Action, Result",
    "origin": null,
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "While "
          },
          {
            "text": "STAR",
            "strong": true
          },
          {
            "text": " is the comprehensive standard for in-depth behavioral interviews and "
          },
          {
            "text": "CARL",
            "strong": true
          },
          {
            "text": " evaluates senior metacognition and learning, many high-stakes situations demand "
          },
          {
            "text": "extreme brevity, high information density, and decisive clarity",
            "strong": true
          },
          {
            "text": "."
          }
        ]
      },
      {
        "kind": "p",
        "runs": [
          {
            "text": "The "
          },
          {
            "text": "PAR Framework",
            "strong": true
          },
          {
            "text": " ("
          },
          {
            "text": "Problem, Action, Result",
            "strong": true
          },
          {
            "text": ") strips away preamble, backstory, and narrative drift. It is designed for:"
          }
        ]
      },
      {
        "kind": "ul",
        "items": [
          {
            "runs": [
              {
                "text": "Initial Recruiter & Screening Phone Rounds",
                "strong": true
              },
              {
                "text": " (where candidates have 45–60 seconds per answer)."
              }
            ]
          },
          {
            "runs": [
              {
                "text": "Executive & C-Suite Briefings",
                "strong": true
              },
              {
                "text": " (where leaders demand rapid bottom-line summaries)."
              }
            ]
          },
          {
            "runs": [
              {
                "text": "Rapid-Fire Technical Panels",
                "strong": true
              },
              {
                "text": " (answering 6–8 behavioral questions in a 30-minute block)."
              }
            ]
          },
          {
            "runs": [
              {
                "text": "Elevator Pitches & Networking Introductions",
                "strong": true
              },
              {
                "text": "."
              }
            ]
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "Framework Comparison: STAR vs. CARL vs. PAR",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Dimension"
                }
              ],
              [
                {
                  "text": "STAR"
                }
              ],
              [
                {
                  "text": "CARL"
                }
              ],
              [
                {
                  "text": "PAR"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "Pacing Budget",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "90–120 seconds"
                  }
                ],
                [
                  {
                    "text": "100–130 seconds"
                  }
                ],
                [
                  {
                    "text": "45–60 seconds (Total)",
                    "strong": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Context Overhead",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "~30% (Situation + Task)"
                  }
                ],
                [
                  {
                    "text": "~20% (Context)"
                  }
                ],
                [
                  {
                    "text": "< 20% (Direct Problem Statement)",
                    "strong": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Core Value",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Methodical execution."
                  }
                ],
                [
                  {
                    "text": "Metacognitive growth & learning."
                  }
                ],
                [
                  {
                    "text": "Executive brevity & signal-to-noise ratio.",
                    "strong": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Primary Audience",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Hiring Managers & Team Leads."
                  }
                ],
                [
                  {
                    "text": "Staff+ Reviewers, Directors, VPs."
                  }
                ],
                [
                  {
                    "text": "Recruiters, Executives, Founders.",
                    "strong": true
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Core Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: Zero Backstory Drift (The 15-Second Problem Rule)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In PAR, the speaker does not spend time describing company origins, team hierarchies, or personal feelings."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "The Problem must be articulated in "
                      },
                      {
                        "text": "1–2 punchy opening sentences",
                        "strong": true
                      },
                      {
                        "text": " (10–15 seconds maximum) identifying the friction point and stakes."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Anti-Pattern (The Creeping Backstory)"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Spending 35 seconds explaining how the company was founded in 2021 before mentioning the bug."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Decisive First-Person Execution (\"I\", Not \"We\")",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Because PAR answers are short, every word counts. Using passive team language (\"We were having a meeting and we decided...\") wastes precious seconds."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "The Action phase must immediately spotlight the candidate's personal initiative and technical choices: "
                      },
                      {
                        "text": "\"I isolated the bottleneck, re-indexed the primary key, and staged a zero-downtime hotfix.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Impact is Mandatory (Both Quantitative & Operational Count)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In keeping with our core philosophy, results do "
                      },
                      {
                        "text": "not",
                        "strong": true
                      },
                      {
                        "text": " need to be solely numeric statistics to receive top scores."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Valid Quantitative Results"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"This cut checkout drop-off by 28% and saved ₦8M in lost weekend orders.\"",
                        "em": true
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Valid Qualitative/Operational Results"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"This unblocked our mobile engineering release, prevented a contract dispute with our banking partner, and restored service before customer support queues were flooded.\"",
                        "em": true
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "What is Penalized"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Ending without a punchline ("
                      },
                      {
                        "text": "\"and then we moved on to the next ticket\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: High Information Density (Signal-to-Noise)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The candidate's delivery should maintain an energetic, concise cadence (140 - 165 WPM) with minimal verbal hesitation (\"um\", \"uh\", \"you know\")."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "SCQA": {
    "id": "SCQA",
    "fullName": "Situation, Complication, Question, Answer",
    "origin": "The SCQA Framework (Situation, Complication, Question, Answer) was created by Barbara Minto at McKinsey & Company (1981) in The Pyramid Principle. It is the undisputed global standard for executive briefings, architecture review proposals (RFCs), investor updates, and C-suite technical memos. Cited in Nasir's The Plan (Sections 2.2.2 & 3.4.2), SCQA operationalizes BLUF (Bottom Line Up Front): structuring ideas so the human brain can process high-stakes technical proposals with zero cognitive friction.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "In technical and corporate leadership, the single most common communication failure is "
          },
          {
            "text": "\"Burying the Lede\"",
            "strong": true
          },
          {
            "text": "—taking the audience on a winding, chronological detective journey before finally revealing the recommendation in the closing seconds."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "Framework Comparison: Narrative (STAR) vs. Structural (SCQA)",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Dimension"
                }
              ],
              [
                {
                  "text": "STAR (Behavioral / Storytelling)"
                }
              ],
              [
                {
                  "text": "SCQA (Minto Pyramid / Strategic)"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "Primary Goal",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Prove past individual competence & execution."
                  }
                ],
                [
                  {
                    "text": "Persuade leadership to adopt a technical/business decision."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Pacing Order",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Chronological past: S → T → A → R."
                  }
                ],
                [
                  {
                    "text": "Logical hierarchy: Common Ground → Friction → Dilemma → "
                  },
                  {
                    "text": "Recommendation",
                    "strong": true
                  },
                  {
                    "text": "."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Context Role",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Establish personal setting & scale."
                  }
                ],
                [
                  {
                    "text": "Establish "
                  },
                  {
                    "text": "uncontroversial agreement",
                    "strong": true
                  },
                  {
                    "text": " before introducing tension."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Primary Audience",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Interviewers, Promotion Panels."
                  }
                ],
                [
                  {
                    "text": "Executives, VPs, CTOs, Board Members, Investors."
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Core Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: The Uncontroversial Baseline Situation",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In Minto's doctrine, the "
                      },
                      {
                        "text": "Situation",
                        "strong": true
                      },
                      {
                        "text": " must be something all stakeholders agree on without debate ("
                      },
                      {
                        "text": "\"As we know, our payment gateway processes ₦200M daily with 99.9% uptime\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "If the speaker opens with a controversial or accusatory claim ("
                      },
                      {
                        "text": "\"Our infrastructure is terrible and we're falling behind\"",
                        "em": true
                      },
                      {
                        "text": "), stakeholders instantly enter cognitive defense mode and stop listening to the recommendation."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: The Acute Complication (The Catalyst)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The "
                      },
                      {
                        "text": "Complication",
                        "strong": true
                      },
                      {
                        "text": " explains why the status quo can no longer hold. It introduces the catalyst: an API deprecation, a cost spike, an upcoming regulatory deadline, or a technical bottleneck."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "It must articulate "
                      },
                      {
                        "text": "the operational stakes of inaction",
                        "strong": true
                      },
                      {
                        "text": " ("
                      },
                      {
                        "text": "\"If unaddressed before Q4, checkout drop-off will spike by 30%\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: BLUF Efficiency (Bottom Line Up Front)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Senior leaders have zero patience for mystery novels. The "
                      },
                      {
                        "text": "Answer",
                        "strong": true
                      },
                      {
                        "text": " must not be buried."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "In spoken briefings, the speaker must transition smoothly through S-C-Q and deliver a clear, actionable "
                      },
                      {
                        "text": "Answer",
                        "strong": true
                      },
                      {
                        "text": " with structured rationale."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Top scores are awarded when the recommendation is stated clearly, decisively, and supported by structured logical pillars."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Actionable Substance (Quantitative & Operational Value)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The "
                      },
                      {
                        "text": "Answer",
                        "strong": true
                      },
                      {
                        "text": " must not be vague hand-waving ("
                      },
                      {
                        "text": "\"We should look into better tools\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "It must propose a concrete, actionable move—whether backed by "
                      },
                      {
                        "text": "quantitative figures",
                        "strong": true
                      },
                      {
                        "text": " ("
                      },
                      {
                        "text": "\"Deploying the multi-region Redis cluster cuts latency by 60% and saves ₦15M\"",
                        "em": true
                      },
                      {
                        "text": ") or "
                      },
                      {
                        "text": "qualitative/operational alignment",
                        "strong": true
                      },
                      {
                        "text": " ("
                      },
                      {
                        "text": "\"Adopting an asynchronous queue decouples our billing pipeline, unblocks the mobile team, and eliminates our single point of failure\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "SBI": {
    "id": "SBI",
    "fullName": "Situation, Behavior, Impact",
    "origin": "The SBI Framework (Situation, Behavior, Impact) was developed by the Center for Creative Leadership (CCL). Grounded in cognitive appraisal theory and behavioral psychology, it is the premier evidence-based model for delivering critique without triggering psychological defensiveness (the amygdala hijack). Cited in Nasir's The Plan (Sections 2.2.8 & 3.4.8), SBI strips away emotional venting and mind-reading, anchoring the feedback in objective reality and operational outcomes.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "The single greatest point of failure in leadership and peer communication is "
          },
          {
            "text": "corrective feedback",
            "strong": true
          },
          {
            "text": ". Traditional feedback almost always triggers defensiveness, denial, and interpersonal hostility because leaders conflate "
          },
          {
            "text": "observable facts",
            "strong": true
          },
          {
            "text": " with "
          },
          {
            "text": "subjective character judgments",
            "strong": true
          },
          {
            "text": "."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "Traditional Feedback vs. SBI Feedback",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Dimension"
                }
              ],
              [
                {
                  "text": "Traditional Flawed Feedback"
                }
              ],
              [
                {
                  "text": "SBI Evidence-Based Feedback"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "Opening",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"You have a bad attitude in meetings.\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"Yesterday during the 10:00 AM sprint retro [Situation]...\"",
                    "em": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Observation",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"You are arrogant, disrespectful, and don't care about the team.\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"...you interrupted the junior engineer three times while she was presenting [Behavior]...\"",
                    "em": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Impact",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"People are annoyed with you.\"",
                    "em": true
                  }
                ],
                [
                  {
                    "text": "\"...as a result, she stopped sharing her architectural findings, and the team lost 20 minutes of root-cause analysis [Impact].\"",
                    "em": true
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Conclusion",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "\"Fix this immediately.\"",
                    "em": true
                  },
                  {
                    "text": " (Dictate)"
                  }
                ],
                [
                  {
                    "text": "\"What was happening from your perspective? How can we handle this better next time? [Co-Creation]\"",
                    "em": true
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Core Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: The \"Camera-Recordable\" Test (Zero Mind-Reading)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "The Golden Rule of SBI"
                      }
                    ],
                    "runs": [
                      {
                        "text": "A valid "
                      },
                      {
                        "text": "Behavior",
                        "strong": true
                      },
                      {
                        "text": " is strictly something a video camera could capture or an audio recorder could transcribe."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Camera-Recordable"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Words spoken, specific interruptions, missed pull requests, arriving 15 minutes late, typing on a phone during a presentation."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "NOT Camera-Recordable (Subjective Judgments)"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"You were lazy\", \"You were dismissive\", \"You had an attitude\", \"You don't respect authority\", \"You lacked commitment\"",
                        "em": true
                      },
                      {
                        "text": ". These are mind-reading assumptions that guarantee defensive pushback."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Precise Situational Anchoring (Banish \"Always\" and \"Never\")",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Feedback must be anchored to a "
                      },
                      {
                        "text": "specific time, meeting, or event",
                        "strong": true
                      },
                      {
                        "text": " ("
                      },
                      {
                        "text": "\"During yesterday's incident war room...\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Sweeping generalizations ("
                      },
                      {
                        "text": "\"You always interrupt people\", \"You never update Jira\"",
                        "em": true
                      },
                      {
                        "text": ") trigger immediate fact-checking arguments ("
                      },
                      {
                        "text": "\"I didn't interrupt last Tuesday!\"",
                        "em": true
                      },
                      {
                        "text": "), completely distracting from the core issue."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Impact Accountability (Both Relational & Operational)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The "
                      },
                      {
                        "text": "Impact",
                        "strong": true
                      },
                      {
                        "text": " explains why the behavior matters. It must articulate the consequence on the team, the system, or the business."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Valid Operational Impact"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"As a result, our staging deployment was blocked for 3 hours and the QA team had to work overtime.\"",
                        "em": true
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Valid Relational/Team Impact"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"As a result, junior engineers felt hesitant to raise safety concerns, damaging our psychological safety.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Banish the \"Feedback Sandwich\"",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The amateur practice of sandwiching criticism between fake compliments ("
                      },
                      {
                        "text": "\"You're a great guy, BUT your code quality is awful, BUT you have great energy\"",
                        "em": true
                      },
                      {
                        "text": ") dilutes the message and breeds organizational cynicism."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "SBI values "
                      },
                      {
                        "text": "clean, respectful directness",
                        "strong": true
                      },
                      {
                        "text": ": state the Situation, describe the Behavior, explain the Impact, and pause."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 5: Co-Authoring the Solution",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Effective feedback is not a lecture; it is an invitation to dialogue."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "The giver pauses and asks curiosity questions: "
                      },
                      {
                        "text": "\"Help me understand what was going on from your side\"",
                        "em": true
                      },
                      {
                        "text": " or "
                      },
                      {
                        "text": "\"What can we do to ensure this doesn't recur?\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "RADICAL_CANDOR": {
    "id": "RADICAL_CANDOR",
    "fullName": "Care Personally, Challenge Directly",
    "origin": "Radical Candor was developed by Kim Scott (former executive at Google and Apple; faculty at Apple University) in Radical Candor: Be a Kick-Ass Boss Without Losing Your Humanity (2017). Cited in Nasir's The Plan (Sections 2.2.8 & 3.4.2), Radical Candor provides a 2×2 behavioral matrix that balances Caring Personally with Challenging Directly.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "In technical organizations, performance conversations usually disintegrate into one of two toxic extremes:"
          }
        ]
      },
      {
        "kind": "ol",
        "items": [
          {
            "label": [
              {
                "text": "The Cruelty of \"Brutal Honesty\" (Obnoxious Aggression)"
              }
            ],
            "runs": [
              {
                "text": "Tearing into people with sarcasm and public humiliation under the guise of \"just being honest.\""
              }
            ]
          },
          {
            "label": [
              {
                "text": "The Cowardice of \"Being Nice\" (Ruinous Empathy)"
              }
            ],
            "runs": [
              {
                "text": "Sugarcoating or withholding critical feedback out of fear of uncomfortable emotions, which lets engineers fail silently until they are abruptly PIP'd or fired."
              }
            ]
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "The Four Quadrants",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Quadrant"
                }
              ],
              [
                {
                  "text": "Care Personally"
                }
              ],
              [
                {
                  "text": "Challenge Directly"
                }
              ],
              [
                {
                  "text": "Observable Behavioral Patterns"
                }
              ],
              [
                {
                  "text": "Organizational Danger"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "Radical Candor",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "High",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "High",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Direct, kind, specific, private critique; addresses the work, not the person; committed to recipient's success."
                  }
                ],
                [
                  {
                    "text": "The Goal:",
                    "strong": true
                  },
                  {
                    "text": " High trust, rapid growth, zero surprises."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Obnoxious Aggression",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Low"
                  }
                ],
                [
                  {
                    "text": "High",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Sarcastic, belittling, public critique; personal insults; zero empathy for the human being."
                  }
                ],
                [
                  {
                    "text": "Breeds fear, turnover, and psychological unsafety."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Ruinous Empathy",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "High",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Low"
                  }
                ],
                [
                  {
                    "text": "Vague, polite hedging; hides errors; offers hollow compliments to protect short-term feelings."
                  }
                ],
                [
                  {
                    "text": "Most Common Danger:",
                    "strong": true
                  },
                  {
                    "text": " People fail silently without knowing why."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "Manipulative Insincerity",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Low"
                  }
                ],
                [
                  {
                    "text": "Low"
                  }
                ],
                [
                  {
                    "text": "Fake flattery to their face; gossip and complaining behind their back; passive-aggressive."
                  }
                ],
                [
                  {
                    "text": "Toxic politics, paranoia, and cultural decay."
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Core Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: Clarity is Kindness (Challenge Directly)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Telling an engineer that their code or architecture is ready when it is riddled with security bugs is not \"kind\"—it is cruel."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Challenging directly means "
                      },
                      {
                        "text": "unambiguous clarity",
                        "strong": true
                      },
                      {
                        "text": ": the listener must walk away knowing "
                      },
                      {
                        "text": "exactly",
                        "em": true
                      },
                      {
                        "text": " what the gap is and what standard is required."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "What is Penalized"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Vague, hesitant hints that leave the recipient confused ("
                      },
                      {
                        "text": "\"Maybe if you have time, consider looking into that\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Sincere Human Dignity (Care Personally)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Caring personally is not fake corporate sentimentality or prying into personal lives. It means acknowledging the person's dignity, validating their effort, and showing that the critique comes from a genuine desire to see them succeed."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "What is Penalized"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Treating the colleague as an expendable cog, using mockery, or enjoying the delivery of harsh news."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Praise in Public, Criticize in Private",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Radical Candor mandates that corrective critique is delivered "
                      },
                      {
                        "text": "privately and immediately",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Public call-outs or dressing-downs in Slack channels or group retros instantly push the interaction into "
                      },
                      {
                        "text": "Obnoxious Aggression",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Solicit Criticism Before Giving It",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "True Radical Candor begins with the leader modeling vulnerability by inviting critique on themselves:"
                      }
                    ],
                    "children": [
                      {
                        "runs": [
                          {
                            "text": "\"Before we dive in, what is one thing I am doing that is making your work harder or blocking you?\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "STATE": {
    "id": "STATE",
    "fullName": "Share facts, Tell your story, Ask, Talk tentatively, Encourage testing",
    "origin": "The STATE Protocol was developed by Kerry Patterson, Joseph Grenny, Ron McMillan, and Al Switzler in Crucial Conversations: Tools for Talking When Stakes Are High (2002), based on 25+ years of research observing the top 5% of organizational communicators. Cited extensively in Nasir's The Plan (Sections 2.2.3 & 3.4.3), STATE provides an operational algorithm for entering high-stakes, emotionally charged dialogue without retreating into silence or escalating into hostility.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "When opinions differ, stakes are high, and emotions run strong, human communication almost invariably devolves into one of two destructive failure modes:"
          }
        ]
      },
      {
        "kind": "ol",
        "items": [
          {
            "label": [
              {
                "text": "Silence (Masking, Avoiding, Withdrawing)"
              }
            ],
            "runs": [
              {
                "text": "Withholding critical truth to preserve surface harmony, allowing architectural flaws, safety violations, or cultural toxicity to fester."
              }
            ]
          },
          {
            "label": [
              {
                "text": "Violence (Controlling, Labeling, Attacking)"
              }
            ],
            "runs": [
              {
                "text": "Forcing one's opinion on others through dogmatic aggression, executive fiat, or emotional intimidation."
              }
            ]
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "The 5 Elements of STATE",
        "blocks": [
          {
            "kind": "table",
            "head": [
              [
                {
                  "text": "Letter"
                }
              ],
              [
                {
                  "text": "Step"
                }
              ],
              [
                {
                  "text": "What to Do"
                }
              ],
              [
                {
                  "text": "What NOT to Do"
                }
              ]
            ],
            "rows": [
              [
                [
                  {
                    "text": "S",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Share your facts",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Lead with the least controversial, most observable, and verifiable data (timestamps, PRs, metric logs, written goals)."
                  }
                ],
                [
                  {
                    "text": "Do NOT lead with emotional conclusions or accusations ("
                  },
                  {
                    "text": "\"You don't care about quality\"",
                    "em": true
                  },
                  {
                    "text": ")."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "T",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Tell your story",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Frame your conclusion as a personal interpretation ("
                  },
                  {
                    "text": "\"The story I'm telling myself is...\", \"It makes me wonder if...\"",
                    "em": true
                  },
                  {
                    "text": ")."
                  }
                ],
                [
                  {
                    "text": "Do NOT present subjective interpretations as incontrovertible facts."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "A",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Ask for their path",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Actively invite their data and perspective ("
                  },
                  {
                    "text": "\"Help me understand how you see it\", \"What was happening from your vantage point?\"",
                    "em": true
                  },
                  {
                    "text": ")."
                  }
                ],
                [
                  {
                    "text": "Do NOT ask rhetorical traps or patronizing cross-examinations."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "T",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Talk tentatively",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Use measured, humble language ("
                  },
                  {
                    "text": "\"It appears to me\", \"Perhaps\", \"I could be missing something\"",
                    "em": true
                  },
                  {
                    "text": ")."
                  }
                ],
                [
                  {
                    "text": "Banish dogmatic absolutes ("
                  },
                  {
                    "text": "\"Obviously\", \"Clearly\", \"You always\", \"There is no doubt\"",
                    "em": true
                  },
                  {
                    "text": ")."
                  }
                ]
              ],
              [
                [
                  {
                    "text": "E",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Encourage testing",
                    "strong": true
                  }
                ],
                [
                  {
                    "text": "Actively invite dissent and counter-evidence ("
                  },
                  {
                    "text": "\"Do you see this differently?\", \"If I've got this wrong, please challenge me\"",
                    "em": true
                  },
                  {
                    "text": ")."
                  }
                ],
                [
                  {
                    "text": "Do NOT fish for forced agreement or nod-along compliance."
                  }
                ]
              ]
            ]
          }
        ]
      },
      {
        "heading": "Core Evaluation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: Master Your Stories (Data → Story → Emotion → Action)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In cognitive psychology, emotions do not come directly from external events; they come from the "
                      },
                      {
                        "text": "story",
                        "strong": true
                      },
                      {
                        "text": " we tell ourselves about the data."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Example Data"
                      }
                    ],
                    "runs": [
                      {
                        "text": "A teammate committed a hotfix directly to main without tests."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Villain Story"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"He thinks he's above the rules and has zero respect for my authority.\"",
                        "em": true
                      },
                      {
                        "text": " (Leads to anger and attack)."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Mastered Story"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"He committed directly to main. He was likely panicking about the downtime. Let me verify why before assuming bad intent.\"",
                        "em": true
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "The speaker must clearly separate "
                      },
                      {
                        "text": "what happened (data)",
                        "strong": true
                      },
                      {
                        "text": " from "
                      },
                      {
                        "text": "what it meant (story)",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Facts are Safe and Persuasive",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "People argue with stories, but they cannot reasonably argue with camera-recordable facts."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Leading with: "
                      },
                      {
                        "text": "\"In the last three sprints, four database PRs were merged without passing CI gates [Fact]\"",
                        "em": true
                      },
                      {
                        "text": " anchors the conversation in objective reality."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Leading with: "
                      },
                      {
                        "text": "\"You have no respect for our engineering standards [Story]\"",
                        "em": true
                      },
                      {
                        "text": " triggers an instant defensive explosion."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Tentative Language is Strength, Not Weakness",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Amateurs believe that being firm requires using words like "
                      },
                      {
                        "text": "\"obviously\"",
                        "em": true
                      },
                      {
                        "text": ", "
                      },
                      {
                        "text": "\"without question\"",
                        "em": true
                      },
                      {
                        "text": ", "
                      },
                      {
                        "text": "\"clearly\"",
                        "em": true
                      },
                      {
                        "text": ", and "
                      },
                      {
                        "text": "\"you always\"",
                        "em": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "High-stakes masters understand that "
                      },
                      {
                        "text": "dogmatic absolutes shut down dialogue",
                        "strong": true
                      },
                      {
                        "text": ". Speaking tentatively ("
                      },
                      {
                        "text": "\"From where I sit, it looks like...\", \"My concern is that...\"",
                        "em": true
                      },
                      {
                        "text": ") demonstrates intellectual security and creates psychological safety while upholding rigorous standards."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Establishing Mutual Purpose",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Before diving into sensitive conflict, the speaker must establish "
                      },
                      {
                        "text": "Mutual Purpose",
                        "strong": true
                      },
                      {
                        "text": " ("
                      },
                      {
                        "text": "\"We both want this launch to succeed without customer downtime\"",
                        "em": true
                      },
                      {
                        "text": ", "
                      },
                      {
                        "text": "\"Our shared goal is keeping this client's trust\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "This eliminates the \"Fool's Choice\" (believing you must choose between speaking the truth or preserving the relationship)."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "GOTTMAN": {
    "id": "GOTTMAN",
    "fullName": "De-escalation and the Four Horsemen",
    "origin": "The Gottman De-escalation Framework was developed by Dr. John Gottman and Dr. Julie Schwartz Gottman (The Gottman Institute). Built on 40+ years of longitudinal laboratory research with a >90% predictive accuracy for relationship and partnership outcomes, it is the most empirically verified interpersonal conflict model in psychological science. Extensively documented and integrated in Nasir's The Plan (Sections 2.2.4, 2.2.9, 3.4.4, & 3.4.9), this protocol translates clinical relationship science into an operational playbook for workplace conflict, co-founder deadlocks, and emotional regulation.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "In high-stakes technical ventures, co-founder conflicts, and executive disagreements, intelligence does not prevent relationship destruction. Technical partners who agree on architecture frequently fail because they enter toxic interpersonal combat when under pressure."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "The Four Horsemen and Their Antidotes",
        "blocks": [
          {
            "kind": "group",
            "heading": "Horseman 1: Criticism → Antidote: Gentle Start-up",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "The Toxic Marker"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Attacking the person's character, personality, or core identity rather than addressing a specific behavior ("
                      },
                      {
                        "text": "\"You are so disorganized, careless, and lazy\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Antidote (Gentle Start-up Formula)"
                      }
                    ],
                    "runs": []
                  }
                ]
              },
              {
                "kind": "p",
                "runs": [
                  {
                    "text": "\"I feel [Emotion] about [Specific Event]. I need [Positive Need].\""
                  }
                ]
              },
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Example"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"I feel overwhelmed when database migrations are deployed without staging tests. I need us to walk through the deployment runbook together.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Horseman 2: Contempt → Antidote: Culture of Appreciation & Equal Standing",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "The Toxic Marker"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Sarcasm, cynicism, name-calling, eye-rolling, sneering, mocking humor, or condescending put-downs. Gottman's research proved that "
                      },
                      {
                        "text": "Contempt is the #1 predictor of partnership dissolution and divorce",
                        "strong": true
                      },
                      {
                        "text": ". It conveys disgust and moral superiority."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Antidote"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Zero tolerance for mockery. Speak from an equal, respectful baseline. Acknowledge the counterpart's past contributions and treat them as an intellectual equal."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Horseman 3: Defensiveness → Antidote: Accepting Responsibility",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "The Toxic Marker"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Playing the blameless victim, making endless excuses, or instantly counter-attacking ("
                      },
                      {
                        "text": "\"I wouldn't have missed the release date if your specifications weren't completely incompetent!\"",
                        "em": true
                      },
                      {
                        "text": "). Defensiveness escalates conflict because the counterpart feels unheard."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Antidote"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Own your piece of the problem—even if it represents only 5% of the fault."
                      }
                    ],
                    "children": [
                      {
                        "label": [
                          {
                            "text": "Example"
                          }
                        ],
                        "runs": [
                          {
                            "text": "\"You make a fair point. I should have flagged that API bottleneck earlier in the week before it delayed the release.\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Horseman 4: Stonewalling → Antidote: Physiological Self-Soothing & Time-out",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "The Toxic Marker"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Tuning out, turning away, folding arms, non-responsiveness, or abruptly exiting the room. Stonewalling occurs when a person experiences "
                      },
                      {
                        "text": "diffuse physiological arousal (flooding)",
                        "strong": true
                      },
                      {
                        "text": ": heart rate exceeding 100 BPM, adrenaline release, and cognitive tunnel vision."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Antidote"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Call a structured, respectful 20-minute time-out to lower heart rate, with a firm commitment to return."
                      }
                    ],
                    "children": [
                      {
                        "label": [
                          {
                            "text": "Example"
                          }
                        ],
                        "runs": [
                          {
                            "text": "\"I'm feeling flooded right now and I want to be constructive. Let's take a 20-minute break to reset, and let's meet back at 2:30 PM to resolve this.\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "heading": "Core Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: Repair Attempts are the Thermostat of Conflict",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "In successful partnerships and teams, conflict does not mean an absence of friction; it is defined by "
                      },
                      {
                        "text": "the frequency and acceptance of Repair Attempts",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "A Repair Attempt is any verbal or emotional gesture that de-escalates tension:"
                      }
                    ],
                    "children": [
                      {
                        "runs": [
                          {
                            "text": "\"Can I take that back? That came out harsher than I intended.\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"Can we pause for a second? I want to make sure I'm hearing you.\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"I hear what you're saying, and you're right about that part.\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "High-scoring communicators actively issue and receive repair attempts."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Soft Start-up Dictates the Outcome",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Gottman's research demonstrated that "
                      },
                      {
                        "text": "96% of conversations end on the exact same emotional trajectory in which they began in the first 3 minutes",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "A harsh start-up guarantees a hostile ending. A soft start-up keeps the nervous system calm and enables collaborative problem-solving."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: The 5:1 Magic Ratio",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "During healthy conflict, resilient partnerships maintain at least "
                      },
                      {
                        "text": "5 positive interactions (validations, nods, appreciations, active listening) for every 1 negative interaction (critique, disagreement)",
                        "strong": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "VOSS": {
    "id": "VOSS",
    "fullName": "Tactical Empathy and Calibrated Questions",
    "origin": "The Tactical Empathy Framework was developed by Chris Voss (former Lead International Kidnapping Negotiator for the FBI) in Never Split the Difference: Negotiating As If Your Life Depended On It (2016). Formally featured in Nasir's The Plan (Sections 2.2.7, 3.4.7, & Table 4.6), Tactical Empathy is an intelligence-gathering protocol. It shifts negotiation from an adversarial tug-of-war to a collaborative problem-solving dynamic where the counterpart does the heavy lifting.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "Traditional negotiation training teaches rational game theory, mathematical compromises, and \"splitting the difference.\" In practice, these methods fail because "
          },
          {
            "text": "human decision-making is driven by unaddressed emotional fears, cognitive biases, and the need for autonomy",
            "strong": true
          },
          {
            "text": "."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "Core Negotiation Principles & Behavioral Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: Negotiation is an Information-Gathering Exercise",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The party doing the most talking is losing the negotiation."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Amateurs attempt to argue, convince, and steamroll. Masters ask calibrated questions and label emotions to uncover the counterpart's \"Black Swans\" (hidden motivations, internal pressures, and constraints)."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Emotion Labeling (Sensory Stems, Banish \"I\")",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "The Rule of Labeling"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Neutralize negative emotions and amplify positive ones by naming them dispassionately using sensory stems:"
                      }
                    ],
                    "children": [
                      {
                        "runs": [
                          {
                            "text": "\"It sounds like you're under intense pressure to hit this deadline.\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"It seems like you feel your team's contributions are being overlooked.\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"It feels like there's a constraint here we haven't discussed yet.\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Toxic Mistake"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Using first-person language ("
                      },
                      {
                        "text": "\"I understand how you feel\"",
                        "em": true
                      },
                      {
                        "text": " or "
                      },
                      {
                        "text": "\"I hear you\"",
                        "em": true
                      },
                      {
                        "text": "). First-person framing centers the speaker and triggers defensive skepticism ("
                      },
                      {
                        "text": "\"No you don't!\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Calibrated \"How\" & \"What\" Questions (Banish \"Why\")",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Passing the Mental Burden"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Calibrated questions use \"How\" or \"What\" to invite the counterpart to solve your problem for you:"
                      }
                    ],
                    "children": [
                      {
                        "runs": [
                          {
                            "text": "\"How am I supposed to do that?\"",
                            "em": true
                          },
                          {
                            "text": " (The supreme non-confrontational pushback)."
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"What about this proposal doesn't work for your team?\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"How does this move us closer to our launch date?\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Banish \"Why\""
                      }
                    ],
                    "runs": [
                      {
                        "text": "In almost every language and culture, \"Why\" triggers instinctual defensiveness ("
                      },
                      {
                        "text": "\"Why did you change the pricing?\"",
                        "em": true
                      },
                      {
                        "text": " → Counterpart feels accused and doubles down). Replace with: "
                      },
                      {
                        "text": "\"What led to the change in pricing?\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: Get to \"No\" Early (Autonomy & Psychological Safety)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Forcing a counterpart to say \"Yes\" ("
                      },
                      {
                        "text": "\"Do you want to save money?\"",
                        "em": true
                      },
                      {
                        "text": ") makes them feel manipulated and defensive."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Saying \"No\" makes humans feel safe, protected, and in control. Voss advocates asking questions engineered for a \"No\":"
                      }
                    ],
                    "children": [
                      {
                        "runs": [
                          {
                            "text": "\"Is this a bad time to talk?\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"Have you completely walked away from this project?\"",
                            "em": true
                          }
                        ]
                      },
                      {
                        "runs": [
                          {
                            "text": "\"Would it be ridiculous to propose a phased rollout?\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 5: The \"Late-Night FM DJ Voice\"",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "When negotiation gets tense, pitch and pace dictate outcomes."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Fast, high-pitched speech conveys anxiety, desperation, or aggression."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "The "
                      },
                      {
                        "text": "Late-Night FM DJ Voice",
                        "strong": true
                      },
                      {
                        "text": " is calm, slow, reassuring, and downward-inflecting. It triggers neuro-chemical calm (oxytocin release) in the listener's brain."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 6: The Ackerman Model & Reciprocal Concessions",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Never Split the Difference"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Splitting the difference in half is a lazy compromise that leaves both sides bitter."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Reciprocity Rule"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Never give away a concession without demanding something in return:"
                      }
                    ],
                    "children": [
                      {
                        "runs": [
                          {
                            "text": "\"If I agree to maintain that SLA, what can you do on contract duration?\"",
                            "em": true
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "SPARKLINE": {
    "id": "SPARKLINE",
    "fullName": "What Is against What Could Be",
    "origin": "The Sparkline Presentation Framework was created by Nancy Duarte in Resonate: Present Visual Stories That Transform Audiences (2010). By reverse-engineering the structural geometry of the greatest speeches in modern history (including Steve Jobs' 2007 iPhone launch, Martin Luther King Jr.'s \"I Have a Dream\", and JFK's Moonshot address), Duarte discovered a hidden, recurring architectural cadence. Formally documented in Nasir's The Plan (Sections 2.2.10 & 3.4.10), the Sparkline structures public speaking as a rhythmic oscillation between the baseline reality and an elevated future.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "Most technical presentations, conference keynotes, and startup pitches fail because they are designed as "
          },
          {
            "text": "informational data dumps",
            "strong": true
          },
          {
            "text": " rather than "
          },
          {
            "text": "narrative transformations",
            "strong": true
          },
          {
            "text": ". Presenters recite feature lists, technical diagrams, and bulleted slides, leaving the audience cognitively overloaded and emotionally uninspired."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "The 5 Structural Pillars of Duarte's Sparkline",
        "blocks": [
          {
            "kind": "ol",
            "items": [
              {
                "label": [
                  {
                    "text": "The Audience is the Hero (The Presenter is the Mentor)"
                  }
                ],
                "runs": [
                  {
                    "text": "The speaker is not Luke Skywalker; the audience is Luke Skywalker. The speaker is Yoda, providing the wisdom and tool that empowers the hero to triumph."
                  }
                ]
              },
              {
                "label": [
                  {
                    "text": "The Rhythmic Oscillation"
                  }
                ],
                "runs": [
                  {
                    "text": "Continuously alternating between "
                  },
                  {
                    "text": "\"What Is\"",
                    "strong": true
                  },
                  {
                    "text": " (the painful, constrained, familiar current reality) and "
                  },
                  {
                    "text": "\"What Could Be\"",
                    "strong": true
                  },
                  {
                    "text": " (the inspiring, transformed alternative)."
                  }
                ]
              },
              {
                "label": [
                  {
                    "text": "The Call to Adventure"
                  }
                ],
                "runs": [
                  {
                    "text": "Explicitly challenging the audience to cross the threshold of change and abandon the status quo."
                  }
                ]
              },
              {
                "label": [
                  {
                    "text": "The S.T.A.R. Moment (Something They'll Always Remember)"
                  }
                ],
                "runs": [
                  {
                    "text": "A dramatized peak moment—a startling demonstration, a shocking metric, a memorable metaphor, or a dramatic reveal (e.g., Steve Jobs pulling the MacBook Air from a manila envelope)."
                  }
                ]
              },
              {
                "label": [
                  {
                    "text": "The New Bliss"
                  }
                ],
                "runs": [
                  {
                    "text": "Concluding with a vivid, inspiring picture of how the world will fundamentally operate if the audience adopts the proposed vision."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "heading": "Core Presentation Principles & Realistic Nuances",
        "blocks": [
          {
            "kind": "group",
            "heading": "Principle 1: The Hook in the First 30 Seconds (Banish Throat-Clearing)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Amateurs waste the first 60 seconds with boring \"throat-clearing\" ("
                      },
                      {
                        "text": "\"Hello, thank you for having me, my name is X and today I'm going to talk about...\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "Sparkline masters hook the audience within 15–30 seconds with a provocative question, a shocking statistic, or an immersive story that reveals the acute friction in \"What Is\"."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 2: Polarization Creates Movement (The Contrast Engine)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "If a pitch stays entirely in \"What Is\", it feels depressing and stagnant."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "If a pitch stays entirely in \"What Could Be\", it feels like ungrounded, utopian vaporware."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Magic is the Alternation"
                      }
                    ],
                    "runs": [
                      {
                        "text": "The contrast between the friction of today and the elegance of tomorrow creates narrative tension that propels the audience forward."
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 3: Concrete Demonstrations Over Abstract Adjectives",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "Rather than saying "
                      },
                      {
                        "text": "\"our software is incredibly fast and efficient\"",
                        "em": true
                      },
                      {
                        "text": ", describe the concrete reality: "
                      },
                      {
                        "text": "\"Right now, your engineers wait 45 minutes for CI test builds to pass [What Is]. With our distributed cache, that drops to 90 seconds [What Could Be].\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Principle 4: The New Bliss Must Feel Achievable",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "runs": [
                      {
                        "text": "The conclusion should not be a corporate shrug ("
                      },
                      {
                        "text": "\"and that's our roadmap\"",
                        "em": true
                      },
                      {
                        "text": ")."
                      }
                    ]
                  },
                  {
                    "runs": [
                      {
                        "text": "It must paint the "
                      },
                      {
                        "text": "New Bliss",
                        "strong": true
                      },
                      {
                        "text": ": the transformed operational standard where the audience achieves victory, peace of mind, or market leadership."
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "MONROE": {
    "id": "MONROE",
    "fullName": "The Five Step Motivated Sequence",
    "origin": "Monroe's Motivated Sequence was formulated by Alan H. Monroe at Purdue University in 1935. Tested across decades of social psychology, rhetoric, and direct-response marketing, it is considered the most reliable, time-tested persuasion algorithm in human communication. Documented in Nasir's The Plan (Sections 2.2.10 & 3.4.10), Monroe's Sequence organizes persuasive speech into a five-step psychological progression that leads the listener naturally and irresistibly from initial curiosity to decisive, frictionless action.",
    "why": [
      {
        "kind": "p",
        "runs": [
          {
            "text": "In high-stakes business pitches, sales demos, and engineering proposals, speakers frequently make a fatal persuasive mistake: "
          },
          {
            "text": "asking for the commitment before establishing the psychological need",
            "strong": true
          },
          {
            "text": ". When an audience is presented with a solution before they feel the urgency of the problem, they experience cognitive resistance and dismiss the proposal as unnecessary or expensive."
          }
        ]
      }
    ],
    "sections": [
      {
        "heading": "The Five Steps of Monroe's Motivated Sequence",
        "blocks": [
          {
            "kind": "group",
            "heading": "Step 1: Attention (Grab the Room in the First 15 Seconds)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Objective"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Shatter audience complacency."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Technique"
                      }
                    ],
                    "runs": [
                      {
                        "text": "A shocking statistic, a provocative question, a vivid human case study, or a dramatic demonstration."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Example"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"Last month, three Nigerian fintechs lost an estimated ₦180M because of a single 45-minute cloud database freeze.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Step 2: Need (Establish Acute Friction & Urgency)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Objective"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Make the listener feel that the status quo is intolerable."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Technique"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Show that the problem directly threatens their revenue, time, stability, or competitive edge. Present concrete evidence and consequences of inaction."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Example"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"Our current legacy architecture cannot handle Black Friday traffic. If we don't refactor our cache layer before November 1st, our checkout failure rate will spike to 35%.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Step 3: Satisfaction (Present the Concrete Solution)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Objective"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Fulfill the need and satisfy objections."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Technique"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Clearly introduce the solution, explain how it works step-by-step, and demonstrate why it directly solves the Need without creating new bottlenecks."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Example"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"We have designed a dual-write Redis cluster proxy. It intercepts all read/write spikes, absorbs 90% of database pressure, and requires zero modifications to our client SDKs.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Step 4: Visualization (Sensory Projection: The Two Futures)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Objective"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Intensify emotional desire by painting contrasting pictures of the future:"
                      }
                    ],
                    "children": [
                      {
                        "label": [
                          {
                            "text": "Positive Visualization"
                          }
                        ],
                        "runs": [
                          {
                            "text": "Paint the vivid picture of success, relief, and victory if the solution is implemented."
                          }
                        ]
                      },
                      {
                        "label": [
                          {
                            "text": "Negative Visualization"
                          }
                        ],
                        "runs": [
                          {
                            "text": "Remind them of the anxiety, chaos, and financial penalty if they do nothing."
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Example"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"Imagine Black Friday with zero Sev-1 alerts, sub-100ms checkout times, and our engineering team enjoying the weekend in peace. Contrast that with last year: 14 hours in an emergency war room, angry executive Slack pings, and thousands of lost transactions.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "kind": "group",
            "heading": "Step 5: Action (The Frictionless Immediate Next Step)",
            "blocks": [
              {
                "kind": "ul",
                "items": [
                  {
                    "label": [
                      {
                        "text": "Objective"
                      }
                    ],
                    "runs": [
                      {
                        "text": "Convert emotional momentum into immediate physical commitment."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "The Golden Rule of Action"
                      }
                    ],
                    "runs": [
                      {
                        "text": "The ask must be "
                      },
                      {
                        "text": "singular, specific, and frictionless",
                        "strong": true
                      },
                      {
                        "text": ". Never give an audience a list of 5 complicated chores. Tell them exactly what to do "
                      },
                      {
                        "text": "today",
                        "em": true
                      },
                      {
                        "text": "."
                      }
                    ]
                  },
                  {
                    "label": [
                      {
                        "text": "Example"
                      }
                    ],
                    "runs": [
                      {
                        "text": "\"I need one approval today: authorize the ₦2M staging environment budget so our team can deploy the proxy for load testing tomorrow morning.\"",
                        "em": true
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
};
