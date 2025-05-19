> ⚠ **Draft for peer commentary**  
> Prepared by **Taha 'supernova_2177' Gungor** (Technical Director) and **May 'MIMI' Kim** (Creative Director) with GPT assistance.  
> **Disclaimer:** AccessAI Tech is incorporated as a for-profit company but is presently operated on a **zero-profit, cost-recovery basis**. Nothing herein is legal advice; consult qualified counsel.

> **Ownership Note:** This white paper and all code in the repository are the personal property of Taha Gungor and May Kim. AccessAI Tech LLC holds rights only to its experimental avatar.

All product and artist names are property of their respective owners and are used here for illustrative purposes only; no endorsement is implied.

# Company-as-Code, Consent-First Personas, and a Zero-Ownership Corporation  
*Public-alpha white paper • May 2025*

## Abstract
This paper describes an **art experiment** that publishes its entire organisational skeleton—charters, policies, helper scripts, and even a provisional brand voice—in a public GitHub repository (**BP-H/code**).

- Transparent policies anyone can inspect.
- Instant updates across all roles.
- 24/7, on-brand responses from each agent.

* **The code layer** (everything that makes the project run) is released under the MIT Licence **owned solely by the individual artists, Taha 'supernova_2177' Gungor and May 'MIMI' Kim**. The MIT form requires all forks to preserve the original attribution line, ensuring creator veto power ([MIT License](https://opensource.org/licenses/MIT)).  
* **The persona layer** (instruction files + deep-knowledge files for every avatar) is licensed **by, and to, the human beings whom those avatars depict** under Creative Commons BY-NC-ND 4.0, which forbids commercial use and derivatives without consent ([CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)).  
* **Example implementation:** *AccessAI Tech*—a sandbox company co-founded by Taha—borrows the MIT code exactly like any outsider and runs an experimental “company GPT” avatar. The repository is a personal sandbox. AccessAI Tech LLC is real but exercises *zero ownership* over sandbox assets.

The result is a **dual-layer, dual-ownership architecture** that allows anyone to fork the organisational blueprint while guaranteeing that no-one can reuse a face or identity without permission.

The entire GitHub repository remains the property of the two artists, while the MIT Licence simply grants the public permission to use the code so long as the attribution line stays intact.

---

## 1 Introduction: From Open-Handbooks to Open-Companies  
Open-handbook pioneers such as **GitLab** ([handbook](https://about.gitlab.com/handbook/)) and **Strapi** ([company handbook](https://strapi.io/company/handbook)) put their employee manuals online for human readers. Our project extends the idea to **machine-readable governance** so that autonomous agents, LLM copilots, or curious hackers can parse, lint, or fork an organisation’s DNA. We call this paradigm **company-as-code**.

Unlike many open projects, we refuse to commingle corporate and creator rights. **The code is MIT and belongs to the two authors; the personas belong to the living muses; any company that appears in the repo—AccessAI Tech included—owns only its logo and a chat avatar that currently speaks in “public-alpha, non-binding” mode.**

---

## 2 Repository Anatomy & Ownership Matrix  

| Layer | Typical Files | Licence | Legal Owner | Why It Matters |
|-------|---------------|---------|-------------|---------------|
| **Operational code** | `/docs/`, `persona_selector.py`, demo site | **MIT** | **Taha Gungor & May Kim (individuals)** | Anyone may fork, resell, or integrate—*provided attribution lines naming the authors are preserved.* |
| **Personas** | `!!!PUBLIC_READ!!!_*_INSTRUCTIONS.txt` + `*_DEEP_KNOWLEDGE_*.txt` | **CC BY-NC-ND 4.0** | **Each human subject** | No commercial use, no derivatives, no omission of credit—ever. |
| **Example avatar (AccessAI Tech)** | `!!!ATTENTION_READ_ALL!!!_COMPANY_GPT_INSTRUCTIONS.txt` | Proprietary, art-only | **AccessAI Tech** | Merely a sandbox; not an official corporate voice and may be retired. |
| **Legal scaffolding** | `LICENSE_SCOPE.md`, `privacy-policy.md`, `DISCLAIMER.md` | n/a | n/a | Takedown procedure, GDPR “right-to-erasure” (Art 17, see <https://gdpr-info.eu/art-17-gdpr/>), plus an explicit note that **no company owns the code**. |

**Key takeaway:** Every company, including AccessAI Tech, uses the MIT code on equal footing with any random fork and cannot re-license what it does not own.

*The company possesses **no** relicensable rights. All IP reverts instantly to the creator upon delivery.*

---

## Corporate Status & IP

AccessAI Tech LLC is a for-profit entity that presently earns no revenue. The company uses the MIT license granted by the artists under the same terms available to the public and claims no ownership over any code, persona, or creative work herein.

### Trademarks

"AccessAI Tech LLC" only owns its own experimental avatar governed by CC BY-NC-ND 4.0. All other names remain property of their respective owners.

### Persona Commercialisation

Each avatar is governed by CC BY-NC-ND 4.0. Paid or derivative use requires a separate, written agreement executed with the persona’s human creator. Granting such permission does not alter the default license for further uses.

---

## 3 Why This Structure Is Unique

* **Zero corporate IP.** Firms can participate without accumulating ownership; they remain tenants in the repository.  
* **Split carrier of rights.** Code → MIT (creators). Identity → CC BY-NC-ND (each person). Corporate avatar → proprietary (company).  
* **Creator veto power.** Because the MIT notice cites only Taha Gungor & May Kim, any hostile takeover would still need their written consent to dual-licence or close-source the project.  
* **Consent-first persona matrix.** Every avatar file begins with an irrevocable clause: “I belong to *my* human; you must ask before remixing me.” This mirrors the objectives of the bipartisan **NO FAKES Act** aimed at safeguarding voice and likeness from unauthorised AI use (<https://www.congress.gov/bill/118th-congress/senate-bill/2770>).  
* **Public-alpha disclaimer for agency.** Each sandbox company avatar states it is *not* a legal representative—avoiding false-authority traps while concepts mature.

---

## 4 Licensing Logic  

| Decision | Rationale |
|----------|-----------|
| **MIT for code** | Short, machine-parsable, and standard. Forces forks to carry the exact attribution line: “© Taha Gungor & May Kim.” (<https://opensource.org/licenses/MIT>) |
| **CC BY-NC-ND 4.0 for personas** | Aligns with right-of-publicity doctrine and the proposed NO FAKES Act protecting individuals from deep-fake exploitation (<https://creativecommons.org/licenses/by-nc-nd/4.0/>; <https://www.congress.gov/bill/118th-congress/senate-bill/2770>). |
| **No licence assignment to any company** | Prevents future investors or managers from claiming authorship of code they did not write. |
| **Proprietary avatar clause** | Allows each company to register a trademark later without contradicting today’s open-source stance. |

---

## 5 Practical Use-Cases  

* **Fork-and-Launch Studio** – A collective clones the repo, swaps in its own personas, and spins up a brand-bot in a weekend—crediting Taha Gungor & May Kim for the scaffolding.  
* **Agent-Readable Term Sheet** – An AutoGPT derivative parses `LICENSE_SCOPE.md` before negotiating a collaboration, ensuring compliance without lawyers.  
* **Sandboxed Celebrity Pitch** – Designers prototype ideas with a Rihanna-style placeholder avatar inside their own fork without publishing it; CC terms block misuse.  
* **Academic Prompt-Injection Testing** – Researchers stress-test the persona “sandwich” structure without touching protected likeness files.  

---

## 6 Governance Roadmap (High-Level)  

| Phase | Status | Milestones |
|-------|--------|------------|
| **Alpha (today)** | ✅ | Public disclaimers; opt-out template; zero corporate IP beyond avatars. |
| **Beta** | ⏳ | Add SPDX tags, JSON-LD for schema.org, CI to auto-stamp attribution into forks. |
| **1.0** | 🔜 | Optional trademarking of individual company avatars; creator sign-off on any binding scope. |
| **2.0** | 🌐 | Decentralised consent registry so each muse can revoke or monetise their avatar on-chain. |

---

## Spawn-Anywhere Protocol

The **Spawn-Anywhere Protocol (SAP)** is our lightweight recipe for booting a persona
in any runtime environment. Each persona folder includes a `manifest.yaml` that
declares the protocol version, an importable Python entrypoint, optional binary
assets, and capability flags such as text or voice. Hosts—from Unreal to Discord—
need only read this manifest and execute the entrypoint to bring the character
online.

SAP keeps things portable. The manifest references a single `launch()` function
that loads the persona files and exposes methods like `generate()` and `speak()`
based on the listed capabilities. Nothing in the host code needs to know how a
particular persona is implemented, so avatars remain drop-in modules.

---

## 7 Frequently Asked Questions

> **Q: Does any company own the MIT code?**  
> **A:** No. The MIT copyright notice names only Taha Gungor and May Kim. Companies merely use the code under the same terms offered to everyone else.

> **Q: What does AccessAI Tech own?**  
> **A:** Only its experimental avatar (COMPANY GPT) and any future trademarks tied to that avatar or to the “AccessAI Tech” name/logo.

> **Q: Can someone fork the repo and strip out Taha & May’s names?**  
> **A:** That violates the MIT attribution clause. Legal remedies exist even in permissive licences.

> **Q: Will future collaborators own their own likeness?**  
> **A:** Yes. Every new persona file references the collaborator’s chosen licence and remains outside corporate ownership.

> **Q: Could a company one day sell this code?**  
> **A:** Only if Taha & May agree to dual-licence. The default MIT terms already allow commercial use by others—provided attribution remains.

> **Q: Are any company avatars legally binding?**  
> **A:** No. Each README labels them “public alpha, non-binding.” Any future agency would require explicit legal ratification.

---

## 8 Conclusion  
This experiment shows a path where **corporations can operate while owning zero intellectual property**. By treating charters as open-source code and refusing to appropriate the creative labour of contributors, we demonstrate that transparency and personal dignity can coexist with viral remix culture.

Fork the scaffolding, build your own house, but keep the architects’ names on the blueprints. That is the simple social contract embedded in **BP-H/code**.
