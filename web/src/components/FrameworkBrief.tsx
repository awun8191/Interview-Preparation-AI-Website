import { useRef, type RefObject } from "react";
import {
  FRAMEWORK_BRIEFS,
  type Block,
  type ListItem,
  type Run,
} from "../data/framework-briefs.generated";
import { FRAMEWORK_SELECTION } from "../data/framework-selection";
import { FRAMEWORKS, type Framework } from "../lib/types";
import { useOverlay } from "../lib/useOverlay";

function Runs({ runs }: { runs: Run[] }) {
  return (
    <>
      {runs.map((run, index) =>
        run.strong ? (
          <strong key={index}>{run.text}</strong>
        ) : run.em ? (
          <em key={index}>{run.text}</em>
        ) : (
          <span key={index}>{run.text}</span>
        ),
      )}
    </>
  );
}

function ListItems({ items }: { items: ListItem[] }) {
  return (
    <>
      {items.map((item, index) => (
        <li key={index}>
          {item.label && (
            <span className="brief-label">
              <Runs runs={item.label} />
            </span>
          )}
          <Runs runs={item.runs} />
          {item.children && item.children.length > 0 && (
            <ul className="brief-sublist">
              {item.children.map((child, childIndex) => (
                <li key={childIndex}>
                  {child.label && (
                    <span className="brief-label">
                      <Runs runs={child.label} />
                    </span>
                  )}
                  <Runs runs={child.runs} />
                </li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </>
  );
}

function Blocks({ blocks }: { blocks: Block[] }) {
  return (
    <>
      {blocks.map((block, index) => {
        if (block.kind === "p") {
          return (
            <p className="brief-p" key={index}>
              <Runs runs={block.runs} />
            </p>
          );
        }

        if (block.kind === "group") {
          return (
            <div className="brief-group" key={index}>
              <h4 className="brief-group-heading">{block.heading}</h4>
              <Blocks blocks={block.blocks} />
            </div>
          );
        }

        if (block.kind === "table") {
          const columnLabels = block.head.slice(1);
          return (
            <div className="brief-rows" key={index}>
              {block.rows.map((row, rowIndex) => {
                const [rowHead, ...values] = row;
                return (
                  <div className="brief-row" key={rowIndex}>
                    {rowHead && (
                      <span className="brief-row-head">
                        <Runs runs={rowHead} />
                      </span>
                    )}
                    {values.map((cell, cellIndex) => {
                      const label = columnLabels[cellIndex];
                      return (
                        <div className="brief-row-field" key={cellIndex}>
                          {label && (
                            <span className="brief-row-label">
                              <Runs runs={label} />
                            </span>
                          )}
                          <span className="brief-row-value">
                            <Runs runs={cell} />
                          </span>
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          );
        }

        const items = <ListItems items={block.items} />;
        return block.kind === "ol" ? (
          <ol className="brief-list" key={index}>
            {items}
          </ol>
        ) : (
          <ul className="brief-list" key={index}>
            {items}
          </ul>
        );
      })}
    </>
  );
}

export function FrameworkBrief({
  framework,
  open,
  onClose,
  triggerRef,
}: {
  framework: Framework;
  open: boolean;
  onClose: () => void;
  triggerRef: RefObject<HTMLElement | null>;
}) {
  const panelRef = useRef<HTMLElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);

  const { trapFocus } = useOverlay<HTMLElement>({
    open,
    onClose,
    panelRef,
    triggerRef,
    initialFocusRef: closeRef,
  });

  const brief = FRAMEWORK_BRIEFS[framework];
  const selection = FRAMEWORK_SELECTION[framework];
  const meta = FRAMEWORKS.find((entry) => entry.id === framework);

  return (
    <>
      <div className="brief-backdrop" data-open={open} onClick={onClose} aria-hidden="true" />
      <aside
        className="brief"
        data-open={open}
        inert={!open}
        role="dialog"
        aria-modal="true"
        aria-labelledby="brief-title"
        ref={panelRef}
        onKeyDown={trapFocus}
      >
        <div className="brief-head">
          <button
            type="button"
            className="drawer-close"
            ref={closeRef}
            onClick={onClose}
            aria-label="Close brief"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
              <path
                d="M6 6l12 12M18 6L6 18"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
          </button>
          <span className="wordmark">The Plan</span>
        </div>

        <div className="brief-body">
          <span className="eyebrow">{meta?.track}</span>
          <h2 className="brief-title" id="brief-title">
            {meta?.name}
          </h2>
          <p className="brief-fullname">{brief.fullName}</p>
          {brief.origin && <p className="brief-origin">{brief.origin}</p>}

          <section className="brief-section">
            <h3 className="brief-heading">Why it exists</h3>
            <Blocks blocks={brief.why} />
          </section>

          {brief.sections.map((section) => (
            <section className="brief-section" key={section.heading}>
              <h3 className="brief-heading">{section.heading}</h3>
              <Blocks blocks={section.blocks} />
            </section>
          ))}

          <section className="brief-section brief-section--selection">
            <h3 className="brief-heading">Reach for this when</h3>
            <ul className="brief-list brief-list--reach">
              {selection.reachFor.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>

            <h3 className="brief-heading">Hold off when</h3>
            <ul className="brief-list brief-list--hold">
              {selection.holdOff.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>

            {selection.pairsWith && <p className="brief-pairs">{selection.pairsWith}</p>}
          </section>
        </div>
      </aside>
    </>
  );
}
