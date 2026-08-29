#!/usr/bin/env python3
"""Render validated lesson JSON as a self-contained, accessible HTML lesson."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from validate_lesson import LessonError, load_and_validate


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def render_list(items: list[str], class_name: str = "plain-list") -> str:
    return f'<ul class="{class_name}">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_flow(visual: dict[str, Any], index: int) -> str:
    nodes = visual.get("nodes", [])
    if not isinstance(nodes, list) or len(nodes) < 2:
        return ""
    steps = "".join(
        f'<li><span class="step-number">{node_index + 1}</span><span>{esc(node)}</span></li>'
        for node_index, node in enumerate(nodes)
    )
    return f"""
    <figure class="visual" aria-labelledby="visual-title-{index}">
      <figcaption>
        <h3 id="visual-title-{index}">{esc(visual.get('title', 'Project flow'))}</h3>
        <p>{esc(visual.get('description', 'A sequence from the current project.'))}</p>
      </figcaption>
      <ol class="flow" aria-label="Flow steps">{steps}</ol>
    </figure>
    """


def render_three(visual: dict[str, Any], index: int) -> str:
    objects = visual.get("objects", [])
    if not isinstance(objects, list) or len(objects) < 2:
        return ""
    safe_objects = []
    labels = []
    for item in objects[:6]:
        if not isinstance(item, dict) or not isinstance(item.get("label"), str):
            continue
        safe_objects.append({"label": item["label"], "color": item.get("color", "warm-gray")})
        labels.append(item["label"])
    if len(safe_objects) < 2:
        return ""
    fallback = "".join(f"<li>{esc(label)}</li>" for label in labels)
    payload = esc(json.dumps(safe_objects, ensure_ascii=False))
    return f"""
    <figure class="visual three-visual" aria-labelledby="visual-title-{index}" data-three-objects="{payload}">
      <figcaption>
        <h3 id="visual-title-{index}">{esc(visual.get('title', 'System relationship'))}</h3>
        <p>{esc(visual.get('description', 'A spatial view of related project parts.'))}</p>
      </figcaption>
      <div class="three-stage" role="img" aria-label="Static relationship view">
        <ul class="relationship-fallback">{fallback}</ul>
        <canvas hidden aria-hidden="true"></canvas>
      </div>
      <div class="visual-actions no-print">
        <button type="button" class="secondary enable-three">Enable 3D view</button>
        <p class="network-note">Optional. This loads a pinned Three.js module from jsDelivr. The lesson is complete without it.</p>
      </div>
      <p class="three-status status" aria-live="polite"></p>
    </figure>
    """


def render_visuals(visuals: Any) -> str:
    if not isinstance(visuals, list):
        return ""
    rendered = []
    for index, visual in enumerate(visuals):
        if not isinstance(visual, dict):
            continue
        if visual.get("type") == "flow":
            rendered.append(render_flow(visual, index))
        elif visual.get("type") == "three-scene":
            rendered.append(render_three(visual, index))
    if not rendered:
        return ""
    return '<section aria-labelledby="visuals-heading"><h2 id="visuals-heading">See the relationship</h2>' + "".join(rendered) + "</section>"


def render_quiz(quiz: list[dict[str, Any]]) -> str:
    blocks = []
    for index, item in enumerate(quiz):
        choices = "".join(
            f'<label><input type="radio" name="question-{index}" value="{choice_index}"> <span>{esc(choice)}</span></label>'
            for choice_index, choice in enumerate(item["choices"])
        )
        blocks.append(
            f"""
            <fieldset class="question" data-answer="{item['answer']}" data-explanation="{esc(item['explanation'])}">
              <legend>{index + 1}. {esc(item['question'])}</legend>
              <div class="choices">{choices}</div>
              <button type="button" class="check-answer">Check answer</button>
              <p class="answer-status status" aria-live="polite"></p>
            </fieldset>
            """
        )
    return "".join(blocks)


def render_html(data: dict[str, Any]) -> str:
    meta = data["meta"]
    summary = data["summary"]
    concepts = "".join(
        f"""
        <article class="concept">
          <h3>{esc(concept['name'])}</h3>
          <p>{esc(concept['plainExplanation'])}</p>
          <p class="project-example"><strong>In this project:</strong> {esc(concept['projectExample'])}</p>
        </article>
        """
        for concept in data["concepts"]
    )
    evidence = ""
    if isinstance(data.get("evidence"), list) and data["evidence"]:
        evidence = '<section aria-labelledby="evidence-heading"><h2 id="evidence-heading">Evidence used</h2>' + render_list(data["evidence"]) + "</section>"
    before_after = ""
    if isinstance(data.get("beforeAfter"), dict):
        item = data["beforeAfter"]
        before_after = f"""
        <section aria-labelledby="change-heading">
          <h2 id="change-heading">Before and after</h2>
          <div class="comparison">
            <div><h3>Before</h3><p>{esc(item.get('before', 'Not provided'))}</p></div>
            <div><h3>After</h3><p>{esc(item.get('after', 'Not provided'))}</p></div>
          </div>
          <p><strong>Why it works:</strong> {esc(item.get('reason', 'Not provided'))}</p>
        </section>
        """
    scope = ", ".join(meta["sourceScope"])
    lesson_json = esc(json.dumps({"threeVersion": "0.180.0"}))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22><rect width=%2232%22 height=%2232%22 rx=%226%22 fill=%22%23657054%22/><path d=%22M9 8h14v3H12v4h9v3h-9v6H9z%22 fill=%22%23FFFDF8%22/></svg>">
  <title>{esc(meta['title'])}</title>
  <style>
    :root {{
      --paper: #F6F1E8;
      --surface: #FFFDF8;
      --ink: #26241F;
      --olive: #657054;
      --olive-dark: #4E5940;
      --terracotta: #A45D3F;
      --gray: #746F66;
      --rule: #D8D0C3;
      --focus: #8A4B33;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font-size: 17px; line-height: 1.68; }}
    a {{ color: var(--olive-dark); text-underline-offset: 0.18em; }}
    button, input {{ font: inherit; }}
    button {{ min-height: 44px; padding: 0.62rem 1rem; border: 1px solid var(--ink); border-radius: 5px; background: var(--ink); color: var(--surface); cursor: pointer; }}
    button:hover {{ background: var(--olive-dark); }}
    button.secondary {{ color: var(--ink); background: transparent; }}
    button.secondary:hover {{ background: #EEE7DC; }}
    button:disabled {{ opacity: 0.62; cursor: default; }}
    button:focus-visible, input:focus-visible {{ outline: 3px solid var(--focus); outline-offset: 3px; }}
    .page {{ width: min(100% - 2rem, 1120px); margin: 0 auto; }}
    header {{ padding: 4.4rem 0 2.2rem; border-bottom: 1px solid var(--rule); }}
    .eyebrow {{ margin: 0 0 0.7rem; color: var(--terracotta); font-size: 0.78rem; font-weight: 750; letter-spacing: 0.09em; text-transform: uppercase; }}
    h1, h2, h3 {{ font-family: Georgia, "Times New Roman", serif; font-weight: 500; line-height: 1.15; text-wrap: balance; }}
    h1 {{ max-width: 17ch; margin: 0; font-size: clamp(2.55rem, 7vw, 5.7rem); letter-spacing: -0.045em; }}
    h2 {{ margin: 0 0 1.4rem; font-size: clamp(1.8rem, 4vw, 2.65rem); letter-spacing: -0.025em; }}
    h3 {{ margin: 0 0 0.65rem; font-size: 1.34rem; }}
    .deck {{ max-width: 62ch; margin: 1.4rem 0 0; color: var(--gray); font-size: 1.12rem; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 0.45rem 1.3rem; margin: 1.6rem 0 0; padding: 0; color: var(--gray); font-size: 0.88rem; list-style: none; }}
    main {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(250px, 0.36fr); gap: clamp(2.2rem, 7vw, 6.5rem); padding: 2.5rem 0 6rem; }}
    .content {{ min-width: 0; max-width: 760px; }}
    section {{ padding: 2.8rem 0; border-bottom: 1px solid var(--rule); }}
    .summary {{ margin: 0 0 0.4rem; padding: clamp(1.4rem, 4vw, 2.2rem); border: 1px solid var(--rule); background: var(--surface); box-shadow: 7px 7px 0 #E4DCCE; }}
    .summary dl {{ display: grid; grid-template-columns: minmax(120px, 0.34fr) 1fr; gap: 1rem 1.5rem; margin: 0; }}
    .summary dt {{ color: var(--terracotta); font-size: 0.77rem; font-weight: 750; letter-spacing: 0.06em; text-transform: uppercase; }}
    .summary dd {{ margin: 0; }}
    .objective {{ font-family: Georgia, "Times New Roman", serif; font-size: 1.48rem; line-height: 1.42; }}
    .concept + .concept {{ margin-top: 2rem; padding-top: 2rem; border-top: 1px dotted var(--rule); }}
    .project-example {{ padding-left: 1rem; border-left: 3px solid var(--olive); }}
    .plain-list {{ padding-left: 1.2rem; }}
    .plain-list li + li {{ margin-top: 0.7rem; }}
    .comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1px; overflow: hidden; margin-bottom: 1.3rem; border: 1px solid var(--rule); background: var(--rule); }}
    .comparison > div {{ padding: 1.3rem; background: var(--surface); }}
    .visual {{ margin: 1.4rem 0 0; padding: 1.4rem 0 0; }}
    .visual figcaption p {{ color: var(--gray); }}
    .flow {{ display: grid; gap: 0; margin: 1.4rem 0 0; padding: 0; list-style: none; }}
    .flow li {{ position: relative; display: grid; grid-template-columns: 2.6rem 1fr; gap: 0.85rem; align-items: center; min-height: 4.2rem; padding: 0.65rem 0; }}
    .flow li:not(:last-child)::after {{ content: ""; position: absolute; top: 3.15rem; bottom: -0.6rem; left: 1.22rem; width: 1px; background: var(--rule); }}
    .step-number {{ position: relative; z-index: 1; display: grid; width: 2.45rem; height: 2.45rem; place-items: center; border: 1px solid var(--olive); border-radius: 50%; background: var(--paper); font-weight: 700; }}
    .three-stage {{ min-height: 250px; display: grid; place-items: center; overflow: hidden; border: 1px solid var(--rule); background: var(--surface); }}
    .three-stage canvas {{ width: 100%; height: 300px; }}
    .relationship-fallback {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 0.8rem; margin: 0; padding: 1.2rem; list-style: none; }}
    .relationship-fallback li {{ max-width: 14rem; padding: 0.8rem 1rem; border: 1px solid var(--rule); border-bottom: 3px solid var(--olive); background: var(--paper); text-align: center; }}
    .visual-actions {{ display: flex; align-items: center; gap: 1rem; margin-top: 0.9rem; }}
    .network-note {{ max-width: 54ch; margin: 0; color: var(--gray); font-size: 0.8rem; line-height: 1.45; }}
    .question {{ margin: 0; padding: 1.5rem 0; border: 0; border-top: 1px solid var(--rule); }}
    .question legend {{ padding: 0 0 0.9rem; font-family: Georgia, "Times New Roman", serif; font-size: 1.22rem; line-height: 1.4; }}
    .choices {{ display: grid; gap: 0.7rem; margin-bottom: 1rem; }}
    .choices label {{ display: flex; gap: 0.6rem; align-items: flex-start; padding: 0.8rem; border: 1px solid transparent; cursor: pointer; }}
    .choices label:has(input:checked) {{ border-color: var(--olive); background: var(--surface); }}
    .choices input {{ margin-top: 0.35rem; accent-color: var(--olive-dark); }}
    .status {{ min-height: 1.6em; color: var(--olive-dark); font-weight: 650; }}
    .transfer {{ padding: 1.4rem 0 0 1.2rem; border-left: 4px solid var(--terracotta); font-family: Georgia, "Times New Roman", serif; font-size: 1.3rem; }}
    aside {{ align-self: start; position: sticky; top: 1.2rem; padding-top: 0.6rem; color: var(--gray); font-size: 0.86rem; }}
    aside h2 {{ color: var(--ink); font-family: inherit; font-size: 0.82rem; font-weight: 750; letter-spacing: 0.06em; text-transform: uppercase; }}
    aside ol {{ margin: 0; padding-left: 1.1rem; }}
    aside li + li {{ margin-top: 0.55rem; }}
    footer {{ padding: 1.5rem 0 3rem; border-top: 1px solid var(--rule); color: var(--gray); font-size: 0.82rem; }}
    @media (max-width: 760px) {{
      header {{ padding-top: 2.8rem; }}
      main {{ display: block; padding-top: 1.5rem; }}
      aside {{ position: static; margin-bottom: 1rem; padding: 1rem 0 1.4rem; border-bottom: 1px solid var(--rule); }}
      .summary dl {{ grid-template-columns: 1fr; gap: 0.25rem; }}
      .summary dd + dt {{ margin-top: 0.8rem; }}
      .comparison {{ grid-template-columns: 1fr; }}
      .visual-actions {{ align-items: flex-start; flex-direction: column; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ scroll-behavior: auto !important; animation: none !important; transition: none !important; }} }}
    @media print {{
      :root, body {{ background: white; }}
      .page {{ width: 100%; }}
      main {{ display: block; }}
      aside, .no-print {{ display: none !important; }}
      section {{ break-inside: avoid; }}
      .summary {{ box-shadow: none; }}
    }}
  </style>
</head>
<body data-lesson-config="{lesson_json}">
  <div class="page">
    <header>
      <p class="eyebrow">Learn while building</p>
      <h1>{esc(meta['title'])}</h1>
      <p class="deck">{esc(data['learningObjective'])}</p>
      <ul class="meta">
        <li><strong>Project:</strong> {esc(meta['project'])}</li>
        <li><strong>Prepared:</strong> {esc(meta['generatedAt'])}</li>
        <li><strong>Sources:</strong> {esc(scope)}</li>
      </ul>
    </header>
    <main>
      <div class="content">
        <section class="summary" aria-labelledby="summary-heading">
          <h2 id="summary-heading">30-second summary</h2>
          <dl>
            <dt>What happened</dt><dd>{esc(summary['whatHappened'])}</dd>
            <dt>Why it matters</dt><dd>{esc(summary['whyItMatters'])}</dd>
            <dt>What changed</dt><dd>{esc(summary['whatChanged'])}</dd>
            <dt>What to learn</dt><dd>{esc(summary['whatToLearn'])}</dd>
            <dt>Verification</dt><dd>{esc(summary['verification'])}</dd>
          </dl>
        </section>
        <section aria-labelledby="objective-heading">
          <h2 id="objective-heading">Your learning goal</h2>
          <p class="objective">{esc(data['learningObjective'])}</p>
        </section>
        {before_after}
        <section aria-labelledby="model-heading">
          <h2 id="model-heading">How to think about it</h2>
          {concepts}
        </section>
        {evidence}
        {render_visuals(data.get('visualizations'))}
        <section aria-labelledby="practice-heading">
          <h2 id="practice-heading">Try it yourself</h2>
          <form>{render_quiz(data['quiz'])}</form>
        </section>
        <section aria-labelledby="transfer-heading">
          <h2 id="transfer-heading">Use the idea again</h2>
          <p class="transfer">{esc(data['transferQuestion'])}</p>
        </section>
      </div>
      <aside aria-labelledby="contents-heading">
        <h2 id="contents-heading">In this lesson</h2>
        <ol>
          <li>Read the short summary</li>
          <li>Build the mental model</li>
          <li>Inspect the project evidence</li>
          <li>Answer without peeking</li>
          <li>Transfer the idea</li>
        </ol>
      </aside>
    </main>
    <footer>This lesson strengthens a foundation. It does not by itself establish professional competence.</footer>
  </div>
  <script>
    document.querySelectorAll('.check-answer').forEach((button) => {{
      button.addEventListener('click', () => {{
        const question = button.closest('.question');
        const selected = question.querySelector('input:checked');
        const status = question.querySelector('.answer-status');
        if (!selected) {{
          status.textContent = 'Choose an answer first.';
          return;
        }}
        const correct = Number(selected.value) === Number(question.dataset.answer);
        status.textContent = `${{correct ? 'That fits the evidence.' : 'Look at the project evidence once more.'}} ${{question.dataset.explanation}}`;
      }});
    }});

    document.querySelectorAll('.enable-three').forEach((button) => {{
      button.addEventListener('click', async () => {{
        const figure = button.closest('.three-visual');
        const status = figure.querySelector('.three-status');
        const canvas = figure.querySelector('canvas');
        button.disabled = true;
        status.textContent = 'Loading the optional 3D view.';
        try {{
          const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js');
          const objects = JSON.parse(figure.dataset.threeObjects);
          const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true, alpha: true }});
          const width = Math.max(320, canvas.parentElement.clientWidth);
          const height = 300;
          renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
          renderer.setSize(width, height, false);
          const scene = new THREE.Scene();
          const camera = new THREE.PerspectiveCamera(44, width / height, 0.1, 100);
          camera.position.set(0, 1.2, 8.5);
          const light = new THREE.DirectionalLight(0xfff4df, 3.2);
          light.position.set(3, 5, 6);
          scene.add(light, new THREE.AmbientLight(0xffffff, 1.8));
          const palette = {{ olive: 0x657054, terracotta: 0xA45D3F, 'warm-gray': 0x746F66 }};
          const group = new THREE.Group();
          objects.forEach((item, index) => {{
            const angle = (index / objects.length) * Math.PI * 2;
            const mesh = new THREE.Mesh(
              new THREE.BoxGeometry(1.25, 1.25, 1.25),
              new THREE.MeshStandardMaterial({{ color: palette[item.color] || palette['warm-gray'], roughness: 0.62 }})
            );
            mesh.position.set(Math.cos(angle) * 2.35, Math.sin(angle * 2) * 0.6, Math.sin(angle) * 1.2);
            group.add(mesh);
          }});
          scene.add(group);
          canvas.hidden = false;
          canvas.setAttribute('aria-hidden', 'false');
          canvas.setAttribute('aria-label', `3D relationship view showing ${{objects.map((item) => item.label).join(', ')}}`);
          const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          let frame = 0;
          const draw = () => {{
            if (!reduced) group.rotation.y += 0.0025;
            group.children.forEach((mesh, index) => {{ mesh.rotation.x = 0.18 + index * 0.12; mesh.rotation.y += reduced ? 0 : 0.0015; }});
            renderer.render(scene, camera);
            if (!reduced && frame < 2400) {{ frame += 1; requestAnimationFrame(draw); }}
          }};
          draw();
          status.textContent = '3D view enabled. The labeled static explanation remains available in the lesson text.';
        }} catch (error) {{
          button.disabled = false;
          status.textContent = 'The 3D view could not load. The static explanation above remains complete.';
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Learn While Building lesson JSON as HTML.")
    parser.add_argument("lesson", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        data = load_and_validate(args.lesson)
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_html(data), encoding="utf-8")
    except (OSError, LessonError) as exc:
        print(f"Could not render lesson: {exc}")
        return 1
    print(f"Rendered lesson: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
