// theme/static_src/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        '../../**/templates/**/*.html', // Looks for templates in ALL of your apps
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require("daisyui")
    ],
}