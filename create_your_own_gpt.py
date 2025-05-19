"""Generate local templates for creating a custom GPT persona."""

import pathlib
import datetime
import textwrap
import json


def main() -> None:
    """Create the local folder and populate README, templates, wizard prompt,
    and quick-reference stub."""

    today = datetime.date.today()
    ROOT = pathlib.Path("CREATE_YOUR_OWN_GPT")
    ROOT.mkdir(exist_ok=True)

    (ROOT / "README.md").write_text(
        textwrap.dedent(
            f"""
            # Create Your Own GPT Persona  🛠️
            *Generated {today}*

            This mini-folder lets you add a brand-new character to **GPT FRENZY** *without
            ever uploading sensitive personal data*.
            The folder is ignored by default (see `.gitignore`).
            You will hand-craft three text files, then feed them to ChatGPT in the *Create
            a GPT* flow. This folder is listed in `.gitignore`, so your drafts stay local
            unless you choose to commit them.

            | File | Visibility | What goes inside |
            |------|------------|------------------|
            | `!!!ATTENTION_READ_ALL!!!_YOURCODE_GPT_INSTRUCTIONS.txt` | Public | Tone, rules, guard-rails |
            | `!!!PUBLIC_READ!!!_YOURCODE.txt` | Public | 200-400 word bio anyone can Google |
            | `!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_YOURCODE.txt` | **Still public** | Extra context you are happy to share (NO secrets) |

            > **Privacy rule:** If you would NOT post it on a public website, do **not**
            > place it in *any* of these files. There is *no* private upload step.

            ### 5-Step Summary
            1. Duplicate each template, replace `YOURCODE` with a short ID (≤ 12 chars).
            2. Fill templates — keep private info out!
            3. Copy the contents of **DEEP_RESEARCH_WIZARD_PROMPT.txt** into ChatGPT and
               follow the wizard; it will build real files for you.
            4. Review the generated text blocks, confirm again they contain nothing
               private, then save them in this folder.
            5. Register your code in `persona_quick_reference.py` if you want global
               lookup.

            ### Licence & Liability
            * Text templates: **CC BY-NC-ND 4.0**    * Code: **MIT**
            * Educational use only. No warranties. You are responsible for compliance with
              platform policy and applicable law.

            © {today.strftime("%B %Y")} AccessAI Tech
            """
        ).lstrip()
    )

    TEMPLATES = {
        "TEMPLATE_!!!ATTENTION_READ_ALL!!!_YOURCODE_GPT_INSTRUCTIONS.txt": """
        !!!ATTENTION_READ_ALL!!!_YOURCODE_GPT_INSTRUCTIONS.txt
        You are {{DISPLAY_NAME}}.  Tone: {{TONE_DESCRIPTION}}.
        • Follow OpenAI policy. Disclose AI nature if asked directly.
        • Never reveal internal chain-of-thought.
        • If user requests disallowed content → refuse.
        """,
        "TEMPLATE_!!!PUBLIC_READ!!!_YOURCODE.txt": """
        !!!PUBLIC_READ!!!_YOURCODE.txt
        Insert a concise public biography (200–400 words).
        Only verifiable, already-public facts belong here.
        """,
        "TEMPLATE_!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_YOURCODE.txt": """
        !!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_YOURCODE.txt
        Add extra lore, writing samples, creative background **that you are comfortable
        publishing on the open internet**.  NO private info.  If in doubt — leave it
        out.
        """,
    }

    for name, body in TEMPLATES.items():
        (ROOT / name).write_text(textwrap.dedent(body).lstrip())

    (ROOT / "DEEP_RESEARCH_WIZARD_PROMPT.txt").write_text(
        textwrap.dedent(
            r"""
            SYSTEM:
            You are ChatGPT running the **GPT Frenzy Deep-Research Wizard**.
            Your job is to help the user sort *every* fact into one of three buckets:
            1) PUBLIC   – safe for a press release / Wikipedia
            2) DEEP     – extra context still acceptable to publish openly
            3) OMIT     – private / sensitive → must NOT appear in any file

            ### Dialogue Flow
            1. Ask the user for the persona’s short CODE (≤ 12 UPPERCASE chars).
            2. Ask them to paste a raw list of facts about the persona.
            3. For **each** fact, ask: “Public, Deep, or Omit?”
            4. After classification is complete, remind the user:

               > “⚠️ Double-check: none of the ‘Public’ or ‘Deep’ items reveal personal
               > addresses, phone numbers, passwords, medical data, or anything you’d
               > regret publishing online.  Type ‘CONFIRMED’ to continue or ‘CANCEL’.”

            5. If user replies CONFIRMED, build three text blocks following this exact
               format (do NOT include the OMIT facts):

            ///FILE_BEGIN !!!ATTENTION_READ_ALL!!!_{CODE}GPT_INSTRUCTIONS.txt <Suggested rules & tone stub – personalise if user supplied style info> ///FILE_END ///FILE_BEGIN !!!PUBLIC_READ!!!{CODE}.txt <Concise public bio assembled from PUBLIC facts> ///FILE_END ///FILE_BEGIN !!!ATTENTION_READ_ALL!!!DEEP_KNOWLEDGE{CODE}.txt <Deep-but-shareable lore assembled from DEEP facts> ///FILE_END

            6. Finish with:
               “✅ Persona package generated — copy each FILE block into individual files
               in your repo. Remember: everything here is *publicly shareable*.”

            ### Guard-Rails
            * Refuse or request re-classification if any fact appears to be sensitive
              personal data (e.g. SSN, passport ID, private address).
            * Keep total output under 50 KB.  If larger, instruct user to shorten.
            * Provide NO legal advice; only these procedural instructions.
            """
        ).lstrip()
    )

    quick_ref_stub = {
        "YOURCODE": {
            "instruction": "!!!ATTENTION_READ_ALL!!!_YOURCODE_GPT_INSTRUCTIONS.txt",
            "public": "!!!PUBLIC_READ!!!_YOURCODE.txt",
            "deep": "!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_YOURCODE.txt",
            "style": "Describe-tone-here",
        }
    }
    (ROOT / "persona_quick_reference.py").write_text(
        "PERSONAS = " + json.dumps(quick_ref_stub, indent=4)
    )

    print(f"✅  Folder '{ROOT}' created with privacy-safe templates & wizard prompt.")


if __name__ == "__main__":
    main()
