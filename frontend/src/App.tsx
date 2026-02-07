import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from "recharts";

const recoveryTrend = [
  { day: "Mon", score: 58 },
  { day: "Tue", score: 61 },
  { day: "Wed", score: 55 },
  { day: "Thu", score: 62 },
  { day: "Fri", score: 65 },
  { day: "Sat", score: 59 },
  { day: "Sun", score: 63 }
];

const volumeTrend = [
  { week: "W1", chest: 14, back: 18 },
  { week: "W2", chest: 16, back: 20 },
  { week: "W3", chest: 15, back: 17 },
  { week: "W4", chest: 18, back: 22 }
];

const recommendations = [
  {
    title: "Reduce shoulder volume by 20%",
    reason: "HRV dropped for 3 days; shoulder volume +18%"
  },
  {
    title: "Add 2 sets of hamstrings",
    reason: "Goal: hypertrophy; current volume below target"
  }
];

export default function App() {
  return (
    <div className="min-h-screen bg-ink text-mist">
      <header className="relative overflow-hidden border-b border-slate/60">
        <div className="absolute -top-24 right-0 h-72 w-72 rounded-full bg-ember/20 blur-3xl" />
        <div className="absolute -bottom-16 left-0 h-64 w-64 rounded-full bg-ocean/20 blur-3xl" />
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-8">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-mist/60">
              Athletica
            </p>
            <h1 className="mt-3 font-display text-4xl font-semibold text-white">
              AI Fitness Analytics
            </h1>
            <p className="mt-2 max-w-xl text-base text-mist/80">
              Explainable recovery, volume, and goal tracking — tuned for a single
              athlete.
            </p>
          </div>
          <div className="hidden items-center gap-6 md:flex">
            <div className="rounded-2xl border border-slate/60 bg-coal/60 px-4 py-3">
              <p className="text-xs uppercase tracking-[0.2em] text-mist/60">
                Goal
              </p>
              <p className="mt-1 text-lg text-white">Lean Bulk</p>
            </div>
            <div className="rounded-2xl border border-slate/60 bg-coal/60 px-4 py-3">
              <p className="text-xs uppercase tracking-[0.2em] text-mist/60">
                Recovery
              </p>
              <p className="mt-1 text-lg text-lime">62 / 100</p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        <section className="grid gap-6 md:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-3xl border border-slate/60 bg-coal/70 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-mist/50">
                  Recovery Trend
                </p>
                <h2 className="mt-2 font-display text-2xl text-white">
                  Weekly Readiness
                </h2>
              </div>
              <span className="rounded-full bg-ember/15 px-3 py-1 text-xs text-ember">
                Light strain week
              </span>
            </div>
            <div className="mt-6 h-56">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={recoveryTrend}>
                  <XAxis dataKey="day" stroke="#6b7280" />
                  <YAxis domain={[40, 80]} stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      background: "#101418",
                      border: "1px solid #252c35",
                      color: "#c7d2e3"
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#4ad0ff"
                    strokeWidth={3}
                    dot={{ r: 4, stroke: "#4ad0ff" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="rounded-3xl border border-slate/60 bg-coal/70 p-6">
            <p className="text-xs uppercase tracking-[0.3em] text-mist/50">
              Today
            </p>
            <h2 className="mt-2 font-display text-2xl text-white">
              Daily Insight
            </h2>
            <div className="mt-6 space-y-4">
              {recommendations.map((item) => (
                <div
                  key={item.title}
                  className="rounded-2xl border border-slate/60 bg-slate/40 p-4"
                >
                  <p className="text-sm font-semibold text-white">
                    {item.title}
                  </p>
                  <p className="mt-2 text-sm text-mist/70">{item.reason}</p>
                  <div className="mt-4 flex gap-3">
                    <button className="rounded-full bg-lime/20 px-4 py-1 text-xs text-lime">
                      Accept
                    </button>
                    <button className="rounded-full bg-ember/20 px-4 py-1 text-xs text-ember">
                      Ignore
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-10 grid gap-6 md:grid-cols-2">
          <div className="rounded-3xl border border-slate/60 bg-coal/70 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-mist/50">
                  Volume Balance
                </p>
                <h3 className="mt-2 font-display text-xl text-white">
                  Weekly Muscle Load
                </h3>
              </div>
              <span className="rounded-full bg-ocean/15 px-3 py-1 text-xs text-ocean">
                Target range
              </span>
            </div>
            <div className="mt-6 h-52">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={volumeTrend}>
                  <XAxis dataKey="week" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      background: "#101418",
                      border: "1px solid #252c35",
                      color: "#c7d2e3"
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="chest"
                    stroke="#ff5c35"
                    fill="#ff5c35"
                    fillOpacity={0.2}
                  />
                  <Area
                    type="monotone"
                    dataKey="back"
                    stroke="#c2f970"
                    fill="#c2f970"
                    fillOpacity={0.2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="rounded-3xl border border-slate/60 bg-coal/70 p-6">
            <p className="text-xs uppercase tracking-[0.3em] text-mist/50">
              Risk Watch
            </p>
            <h3 className="mt-2 font-display text-xl text-white">
              Indicators
            </h3>
            <ul className="mt-6 space-y-3 text-sm text-mist/80">
              <li className="rounded-2xl border border-slate/60 bg-slate/40 px-4 py-3">
                Plateau probability: 0.34 (moderate)
              </li>
              <li className="rounded-2xl border border-slate/60 bg-slate/40 px-4 py-3">
                HRV downtrend: -6.1% (last 7 days)
              </li>
              <li className="rounded-2xl border border-slate/60 bg-slate/40 px-4 py-3">
                Sleep efficiency: 89% (within target)
              </li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  );
}
