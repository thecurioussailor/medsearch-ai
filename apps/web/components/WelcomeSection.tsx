export function WelcomeSection() {
  return (
    <section aria-labelledby="welcome-heading" className="text-center">
      <p className="text-xs font-medium uppercase tracking-[0.14em] text-accent">
        Conversational evidence search
      </p>
      <h1
        id="welcome-heading"
        className="mt-3 font-serif text-[2rem] leading-[1.15] tracking-tight text-ink text-balance sm:text-[2.75rem] lg:text-5xl"
      >
        Find answers in medical evidence.
      </h1>
      <p className="mx-auto mt-3 max-w-xl text-base leading-relaxed text-muted text-pretty sm:text-[17px]">
        Ask questions about diabetes monitoring guidance and explore the source
        passages behind every answer.
      </p>
    </section>
  );
}
