/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"] ,
  theme: {
    extend: {
      colors: {
        ink: "#101418",
        coal: "#171c22",
        slate: "#252c35",
        mist: "#c7d2e3",
        ember: "#ff5c35",
        lime: "#c2f970",
        ocean: "#4ad0ff"
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Source Sans 3'", "sans-serif"]
      }
    }
  },
  plugins: []
};
