# Workflow Execution Plan: project-setup

**Generated:** 2026-03-20  
**Repository:** intel-agency/workflow-orchestration-queue-yankee89-b  
**Dynamic Workflow:** project-setup  
**Trigger:** Pre-build dev container image workflow completed successfully on main branch

---

## 1. Overview

This document provides a comprehensive execution plan for the `project-setup` dynamic workflow. The workflow orchestrates the initialization and setup of the **workflow-orchestration-queue (OS-APOW)** system—a headless agentic orchestration platform that transforms GitHub Issues into automated execution orders.

The workflow follows a structured sequence of assignments that progressively build the repository infrastructure, create planning documentation, establish project structure, and produce AI agent context files.

### Workflow Structure

```
project-setup Dynamic Workflow
├── [PRE-SCRIPT-BEGIN EVENT]
│   └── create-workflow-plan ← CURRENT ASSIGNMENT
├── [MAIN SCRIPT]
│   ├── init-existing-repository
│   ├── create-app-plan
│   ├── create-project-structure
│   ├── create-repository-summary
│   ├── create-agents-md-file
│   └── debrief-and-document
└── [POST-ASSIGNMENT-COMPLETE EVENT]
    ├── validate-assignment-completion
    └── report-progress
```

---

## 2. Project Context Summary

### 2.1 Project Overview

**workflow-orchestration-queue (OS-APOW)** is a groundbreaking headless agentic orchestration platform that transforms "interactive" AI coding into autonomous background production service. The system eliminates human-in-the-loop dependency by translating standard project management artifacts (GitHub Issues, Epics) into automated Execution Orders.

### 2.2 Architecture: Four Pillars

| Pillar | Component | Technology | Purpose |
|--------|-----------|------------|---------|
| **The Ear** | Work Event Notifier | FastAPI, Pydantic | Webhook ingestion, event triage |
| **The State** | Work Queue | GitHub Issues/Labels | Distributed state management |
| **The Brain** | Sentinel Orchestrator | Python Async, httpx | Polling, task claiming, lifecycle management |
| **The Hands** | Opencode Worker | DevContainer, LLM | Code execution, PR creation |

### 2.3 Technology Stack

| Category | Technology | Version |
|----------|------------|---------|
| Language | Python | 3.12+ |
| Web Framework | FastAPI | Latest |
| ASGI Server | Uvicorn | Latest |
| Data Validation | Pydantic | Latest |
| HTTP Client | httpx | Latest |
| Package Manager | uv | Latest |
| Containerization | Docker, DevContainers | Latest |
| CLI Tools | opencode, gh, git | Various |

### 2.4 Development Phases

| Phase | Name | Description | Status |
|-------|------|-------------|--------|
| 0 | Seeding & Bootstrapping | Manual template clone and environment setup | **Current** |
| 1 | The Sentinel (MVP) | Polling engine, shell-bridge execution | Planned |
| 2 | The Ear (Webhook) | FastAPI webhook receiver | Planned |
| 3 | Deep Orchestration | Hierarchical decomposition, self-healing | Planned |

### 2.5 Key Architectural Decisions (ADRs)

- **ADR 07:** Shell-Bridge Execution via `devcontainer-opencode.sh` (not Docker SDK)
- **ADR 08:** Polling-First Resiliency Model (webhooks as optimization)
- **ADR 09:** Provider-Agnostic Interface Layer (ITaskQueue ABC)

### 2.6 Planning Documents Inventory

| Document | Description | Location |
|----------|-------------|----------|
| Development Plan v4.2 | Phased roadmap, user stories, risk assessment | `plan_docs/OS-APOW Development Plan v4.2.md` |
| Architecture Guide v3.2 | System diagrams, ADRs, data flow | `plan_docs/OS-APOW Architecture Guide v3.2.md` |
| Implementation Spec v1.2 | Features, test cases, requirements | `plan_docs/OS-APOW Implementation Specification v1.2.md` |
| Plan Review | Code review findings, improvement recommendations | `plan_docs/OS-APOW Plan Review.md` |
| Simplification Report v1 | Applied simplifications (S-3 through S-11 implemented) | `plan_docs/OS-APOW Simplification Report v1.md` |

### 2.7 Reference Implementation Files

| File | Purpose |
|------|---------|
| `plan_docs/orchestrator_sentinel.py` | Sentinel Orchestrator reference implementation |
| `plan_docs/notifier_service.py` | FastAPI webhook receiver reference implementation |
| `plan_docs/src/models/work_item.py` | Unified WorkItem data model with credential scrubbing |
| `plan_docs/src/queue/github_queue.py` | GitHub queue implementation with connection pooling |

---

## 3. Assignment Execution Plan

### 3.1 Main Script Assignments

#### Assignment 1: init-existing-repository

| Attribute | Details |
|-----------|---------|
| **Goal** | Initialize repository infrastructure (GitHub Project, labels, file renaming) |
| **Prerequisites** | GitHub authentication with scopes: `repo`, `project`, `read:project`, `read:user`, `user:email` |
| **Dependencies** | None (first assignment) |
| **Estimated Complexity** | Medium |

**Acceptance Criteria:**
1. PR and new branch created (`dynamic-workflow-project-setup`)
2. GitHub Project created for issue tracking
3. Project linked to repository with columns: Not Started, In Progress, In Review, Done
4. Labels imported from `.labels.json`
5. Workspace and devcontainer files renamed to match project name

**Key Steps:**
- Create GitHub Project (Board template)
- Import labels using `scripts/import-labels.ps1`
- Rename `ai-new-app-template.code-workspace` → `<repo-name>.code-workspace`
- Update `.devcontainer/devcontainer.json` name property
- Create working branch for all subsequent changes

**Outputs:**
- GitHub Project (issue tracking)
- Imported labels
- Renamed workspace files
- Working branch: `dynamic-workflow-project-setup`

---

#### Assignment 2: create-app-plan

| Attribute | Details |
|-----------|---------|
| **Goal** | Create comprehensive application plan from template documents |
| **Prerequisites** | Application template in `plan_docs/ai-new-app-template.md` (if exists) |
| **Dependencies** | `init-existing-repository` (needs project structure) |
| **Estimated Complexity** | High |

**Acceptance Criteria:**
1. Application template analyzed and understood
2. Project structure documented in `plan_docs/tech-stack.md` and `plan_docs/architecture.md`
3. Plan follows specified technology stack and design principles
4. All phases documented with detailed steps
5. Risks and mitigations identified
6. Planning issue created using template
7. Milestones created and linked to issues
8. `implementation:ready` label applied

**Key Steps:**
- Analyze `plan_docs/` documents for requirements
- Document tech stack in `plan_docs/tech-stack.md`
- Document architecture in `plan_docs/architecture.md`
- Create GitHub Issue with plan using `.github/ISSUE_TEMPLATE/application-plan.md`
- Create milestones for each phase
- Link issues to appropriate milestones

**Events:**
- `pre-assignment-begin` → `gather-context` assignment
- `on-assignment-failure` → `recover-from-error` assignment
- `post-assignment-complete` → `report-progress` assignment

**Outputs:**
- `plan_docs/tech-stack.md`
- `plan_docs/architecture.md`
- Planning Issue (epic)
- Project milestones

**Important:** This is PLANNING ONLY—no code implementation.

---

#### Assignment 3: create-project-structure

| Attribute | Details |
|-----------|---------|
| **Goal** | Create actual solution scaffolding and infrastructure foundation |
| **Prerequisites** | Completed application plan |
| **Dependencies** | `create-app-plan` (needs the plan) |
| **Estimated Complexity** | High |

**Acceptance Criteria:**
1. Solution structure created following guidelines
2. All required project files and directories established
3. Initial configuration files created (global.json, Docker, etc.)
4. Basic CI/CD pipeline structure established
5. Documentation structure created
6. Development environment validated
7. Initial commit made
8. Stakeholder approval obtained
9. Repository summary created

**Key Steps:**
1. **Create Solution Structure**
   - Set up `pyproject.toml` for uv dependencies
   - Create `src/` directory structure
   - Configure project settings
   
2. **Establish Infrastructure Foundation**
   - Create/update Dockerfile
   - Create docker-compose.yml
   - Set up configuration templates
   
3. **Create Development Environment**
   - Environment setup scripts
   - Test project structure
   - Build and development tools
   
4. **Establish Documentation Structure**
   - Comprehensive README.md
   - docs/ directory
   - API documentation structure
   
5. **Initialize CI/CD Foundation**
   - GitHub workflows
   - Quality gates
   
6. **Create Repository Summary**
   - `.ai-repository-summary.md` at root
   - Linked from README.md

**Expected Project Structure:**
```
workflow-orchestration-queue/
├── pyproject.toml
├── uv.lock
├── src/
│   ├── notifier_service.py
│   ├── orchestrator_sentinel.py
│   ├── models/
│   │   └── work_item.py
│   └── queue/
│       └── github_queue.py
├── scripts/
│   ├── devcontainer-opencode.sh
│   ├── gh-auth.ps1
│   └── update-remote-indices.ps1
├── local_ai_instruction_modules/
├── docs/
└── .ai-repository-summary.md
```

**Outputs:**
- Complete project scaffolding
- Docker/CI/CD configuration
- Documentation structure
- Initial commit

---

#### Assignment 4: create-repository-summary

| Attribute | Details |
|-----------|---------|
| **Goal** | Create `.ai-repository-summary.md` for AI agent onboarding |
| **Prerequisites** | Project structure exists |
| **Dependencies** | `create-project-structure` |
| **Estimated Complexity** | Medium |

**Acceptance Criteria:**
1. Summary file exists at repository root
2. Build/test commands documented and validated
3. Project layout described
4. Commands have been verified to work
5. File under 32K tokens (preferably 8-16K)

**Key Steps:**
- Inventory codebase (README, CONTRIBUTING, scripts, workflows)
- Validate and document build commands
- Document project layout and architecture
- Record any workarounds or common pitfalls
- Validate all commands by running them

**Required Sections:**
- Project Overview
- Setup Commands (install, build, run, test, lint)
- Project Structure / Directory Layout
- Code Style conventions
- Testing Instructions
- Common Pitfalls

**Outputs:**
- `.ai-repository-summary.md`

---

#### Assignment 5: create-agents-md-file

| Attribute | Details |
|-----------|---------|
| **Goal** | Create `AGENTS.md` following open AGENTS.md specification |
| **Prerequisites** | Repository initialized, project structure created |
| **Dependencies** | `create-repository-summary` (leverage context) |
| **Estimated Complexity** | Low |

**Acceptance Criteria:**
1. `AGENTS.md` exists at repository root
2. Project overview section present
3. Setup/build/test commands validated
4. Code style conventions documented
5. Project structure section included
6. Testing instructions provided
7. PR/commit guidelines (if applicable)
8. File committed and pushed

**Key Steps:**
1. Gather project context from existing docs
2. Validate build and test commands
3. Draft AGENTS.md following template structure
4. Cross-reference with README.md and `.ai-repository-summary.md`
5. Validate all commands
6. Commit to working branch

**Template Structure:**
- Project Overview
- Setup Commands
- Project Structure
- Code Style
- Testing Instructions
- Architecture Notes
- PR and Commit Guidelines
- Common Pitfalls

**Outputs:**
- `AGENTS.md`

---

#### Assignment 6: debrief-and-document

| Attribute | Details |
|-----------|---------|
| **Goal** | Comprehensive debriefing with lessons learned |
| **Prerequisites** | All main assignments complete |
| **Dependencies** | All previous assignments |
| **Estimated Complexity** | Medium |

**Acceptance Criteria:**
1. Detailed report created following template
2. All 12 sections complete
3. All deviations from assignments documented
4. Execution trace saved
5. Report reviewed and approved
6. Committed to repository

**Required Report Sections:**
1. Executive Summary
2. Workflow Overview (table of all assignments)
3. Key Deliverables
4. Lessons Learned
5. What Worked Well
6. What Could Be Improved
7. Errors Encountered and Resolutions
8. Complex Steps and Challenges
9. Suggested Changes (by category)
10. Metrics and Statistics
11. Future Recommendations
12. Conclusion

**Key Steps:**
- Create report using structured template
- Document all deviations from assignments
- Create execution trace (`debrief-and-document/trace.md`)
- Review with stakeholder
- Commit and push

**Outputs:**
- Debrief report (`.md` file)
- `debrief-and-document/trace.md`
- Continuous improvement cycle initiated

---

### 3.2 Event Assignments

#### Assignment 7: validate-assignment-completion

| Attribute | Details |
|-----------|---------|
| **Trigger** | `post-assignment-complete` event after each main assignment |
| **Goal** | Validate assignment acceptance criteria are met |
| **Executor** | Independent QA agent (not original implementer) |

**Acceptance Criteria:**
1. All required files from assignment exist
2. All verification commands pass
3. Validation report created
4. Pass/fail status determined
5. Remediation steps provided if failed

**Validation Steps:**
1. Identify assignment to validate
2. Read assignment acceptance criteria
3. Verify file outputs exist
4. Run verification commands (build, test, lint)
5. Check exit codes
6. Create validation report
7. Determine pass/fail status

**Validation Report Location:**
`docs/validation/VALIDATION_REPORT_<assignment-name>_<timestamp>.md`

**Output Status Types:**
- ✅ PASSED: All criteria met
- ⚠️ WARNINGS: Critical criteria met, minor warnings
- ❌ FAILED: One or more criteria not met

---

#### Assignment 8: report-progress

| Attribute | Details |
|-----------|---------|
| **Trigger** | `post-assignment-complete` event after each main assignment |
| **Goal** | Progress reporting, output capture, checkpointing |

**Acceptance Criteria:**
1. Structured progress report generated
2. Step outputs captured for subsequent steps
3. Validation checks passed
4. Workflow state checkpointed
5. User notification provided (optional)

**Progress Report Format:**
```
=== STEP COMPLETE: <step-name> ===
Status: ✓ COMPLETE
Duration: <elapsed-time>
Outputs:
  - <key-output-1>: <value-or-location>
  - <key-output-2>: <value-or-location>
Progress: <completed-steps>/<total-steps> (<percentage>%)
Next: <next-step-name>
```

**Key Steps:**
1. Generate progress report
2. Capture step outputs
3. Validate acceptance criteria
4. Create checkpoint state
5. Provide user notification (if applicable)

---

## 4. Sequencing Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROJECT-SETUP WORKFLOW SEQUENCE                          │
└─────────────────────────────────────────────────────────────────────────────┘

[PRE-SCRIPT-BEGIN]
       │
       ▼
┌──────────────────────┐
│ create-workflow-plan │ ◄── CURRENT
└──────────────────────┘
       │
       │ (Plan committed)
       ▼
[MAIN SCRIPT]
       │
       ▼
┌──────────────────────────┐     ┌────────────────────────┐
│ init-existing-repository │────►│ validate-assignment    │
└──────────────────────────┘     │ report-progress        │
       │                         └────────────────────────┘
       ▼
┌──────────────────────┐         ┌────────────────────────┐
│ create-app-plan      │────────►│ validate-assignment    │
└──────────────────────┘         │ report-progress        │
       │                         └────────────────────────┘
       ▼
┌──────────────────────────┐     ┌────────────────────────┐
│ create-project-structure │────►│ validate-assignment    │
└──────────────────────────┘     │ report-progress        │
       │                         └────────────────────────┘
       ▼
┌───────────────────────────┐    ┌────────────────────────┐
│ create-repository-summary │───►│ validate-assignment    │
└───────────────────────────┘    │ report-progress        │
       │                         └────────────────────────┘
       ▼
┌───────────────────────┐        ┌────────────────────────┐
│ create-agents-md-file │───────►│ validate-assignment    │
└───────────────────────┘        │ report-progress        │
       │                         └────────────────────────┘
       ▼
┌────────────────────────┐       ┌────────────────────────┐
│ debrief-and-document   │──────►│ validate-assignment    │
└────────────────────────┘       │ report-progress        │
       │                         └────────────────────────┘
       ▼
[POST-ASSIGNMENT-COMPLETE]
       │
       ▼
┌─────────────────────────────┐
│ validate-assignment-        │ (Final validation)
│ completion                  │
└─────────────────────────────┘
       │
       ▼
┌─────────────────┐
│ report-progress │ (Final progress report)
└─────────────────┘
       │
       ▼
   [COMPLETE]
```

---

## 5. Dependency Graph

```
create-workflow-plan (PRE-EVENT)
         │
         ▼
init-existing-repository ──────────────────────────────────────┐
         │                                                      │
         ▼                                                      │
create-app-plan ◄──────────────────────────────────────────────┤
         │                                                      │
         ▼                                                      │
create-project-structure ◄─────────────────────────────────────┤
         │                                                      │
         ├──────────────────────────────────┐                   │
         ▼                                  ▼                   │
create-repository-summary          create-agents-md-file        │
         │                                  │                   │
         └──────────────┬───────────────────┘                   │
                        ▼                                       │
              debrief-and-document ◄────────────────────────────┘
                        │
                        ▼
         [validate-assignment-completion × 6]
                        │
                        ▼
              [report-progress × 6]
```

---

## 6. Open Questions

### 6.1 Technology Stack Clarification

**Question:** The planning documents describe a Python/FastAPI system, but `create-project-structure` assignment mentions .NET solution structure in its example.

**Impact:** Determines whether to create Python project structure (`pyproject.toml`, `src/`) or .NET structure (`.sln`, `.csproj`).

**Recommendation:** Based on the OS-APOW planning documents, this is a **Python project**. The .NET example in the assignment template should be adapted for Python/FastAPI structure.

---

### 6.2 Reference Implementation Handling

**Question:** The `plan_docs/` directory contains reference implementations (`orchestrator_sentinel.py`, `notifier_service.py`, `src/`). Should these be moved to the main `src/` directory during `create-project-structure`, or remain as reference only?

**Impact:** Affects how `create-project-structure` scaffolds the actual implementation.

**Recommendation:** Move reference implementations from `plan_docs/` to `src/` during project structure creation, as they represent the intended final structure.

---

### 6.3 GitHub App Configuration

**Question:** The assignments require GitHub App authentication with specific scopes (`repo`, `project`, `read:project`, `read:user`, `user:email`). Has the GitHub App been configured for this repository?

**Impact:** `init-existing-repository` may fail if authentication is not properly configured.

**Action Required:** Verify GitHub App installation and permissions before proceeding.

---

### 6.4 Environment Variables

**Question:** The Sentinel requires `GITHUB_TOKEN`, `GITHUB_ORG`, `GITHUB_REPO`, and optionally `SENTINEL_BOT_LOGIN`. Are these configured as repository secrets?

**Impact:** Required for the orchestrator to function in later phases.

**Action Required:** Document required secrets in the application plan.

---

### 6.5 Branch Strategy

**Question:** The `init-existing-repository` assignment creates a branch named `dynamic-workflow-project-setup`. Should all subsequent assignments commit to this same branch?

**Impact:** Determines PR/merge strategy for the workflow.

**Recommendation:** Yes, all assignments should commit to `dynamic-workflow-project-setup` branch, with a single PR created at workflow completion.

---

### 6.6 Missing Files

**Question:** Several files are referenced but may not exist:
- `.labels.json` (for label import)
- `.github/ISSUE_TEMPLATE/application-plan.md` (for planning issue)
- `plan_docs/ai-new-app-template.md` (for application template)

**Impact:** Assignments may fail if expected files are missing.

**Action Required:** Verify file existence or create fallback procedures.

---

### 6.7 DevContainer Operational Status

**Question:** The trigger indicates "Pre-build dev container image workflow completed." Is the devcontainer fully operational and accessible?

**Impact:** Affects ability to validate commands during `create-repository-summary` and `create-agents-md-file`.

**Recommendation:** Verify devcontainer is running and accessible before proceeding with command validation steps.

---

## 7. Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| GitHub API rate limiting | High | Medium | Use GitHub App tokens (5,000 req/hr), implement backoff |
| Missing prerequisite files | Medium | Medium | Create fallback templates, graceful degradation |
| Authentication failures | High | Low | Pre-validate auth with `scripts/test-github-permissions.ps1` |
| Long-running agent tasks | Medium | Medium | Implement heartbeat system per plan docs |
| Model divergence between components | Medium | Low | Use unified `src/models/work_item.py` |

---

## 8. Next Steps

1. **Review this plan** with stakeholder for approval
2. **Resolve open questions** (Section 6) before proceeding
3. **Execute `init-existing-repository`** assignment
4. **Continue sequentially** through main script assignments
5. **Monitor validation** after each assignment
6. **Complete debrief** at workflow end

---

**Plan Prepared By:** Planner Agent  
**Date:** 2026-03-20  
**Status:** Ready for Review  
**Next Action:** Stakeholder approval → `init-existing-repository`
