import type { Config } from "tailwindcss";
const config: Config = { content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"], theme: { extend: { colors: { ink: "#0d1117", panel: "#141a22", line: "#26313d", mint: "#78e2c0", signal: "#f4b860" } } }, plugins: [] };
export default config;
