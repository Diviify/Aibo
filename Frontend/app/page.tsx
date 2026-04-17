export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center overflow-hidden px-6 py-16">
      <section className="w-full max-w-4xl rounded-[2rem] border border-white/60 bg-white/85 p-10 shadow-[0_30px_80px_rgba(43,76,98,0.12)] backdrop-blur">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.35em] text-[var(--color-accent)]">
            Aibo Travel
          </p>
          <h1 className="mt-6 text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
            Next.js frontend is ready for the travel dating experience.
          </h1>
          <p className="mt-6 text-lg leading-8 text-slate-600">
            The project has been initialized with App Router, Tailwind CSS, and
            a clean folder structure for auth, discovery, shared components, and
            API services.
          </p>
        </div>
      </section>
    </main>
  );
}
