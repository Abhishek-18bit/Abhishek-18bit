import { readFile, writeFile } from "node:fs/promises";

const quotes = [
  ["Great things are done by a series of small things brought together.", "Vincent van Gogh"],
  ["The best way to predict the future is to invent it.", "Alan Kay"],
  ["First, solve the problem. Then, write the code.", "John Johnson"],
  ["Simplicity is the soul of efficiency.", "Austin Freeman"],
  ["Success is the sum of small efforts, repeated day in and day out.", "Robert Collier"],
  ["Learning never exhausts the mind.", "Leonardo da Vinci"],
  ["The only way to do great work is to love what you do.", "Steve Jobs"],
  ["It always seems impossible until it is done.", "Nelson Mandela"],
  ["Well begun is half done.", "Aristotle"],
  ["Make it work, make it right, make it fast.", "Kent Beck"],
];

const funFacts = [
  "The first computer bug was an actual moth found in a relay of the Harvard Mark II in 1947.",
  "The first website is still online and was published by Tim Berners-Lee in 1991.",
  "JavaScript was created in just 10 days in 1995.",
  "The first 1 GB hard drive weighed more than 500 pounds.",
  "The word 'algorithm' comes from the name of the Persian mathematician Al-Khwarizmi.",
  "Python is named after Monty Python, not the snake.",
  "Email existed before the World Wide Web.",
  "The original name for Java was Oak.",
  "The first webcam monitored a coffee pot at the University of Cambridge.",
  "Over half of all websites use JavaScript in the browser.",
];

const dayIndex = Math.floor(Date.now() / 86_400_000);
const [quote, author] = quotes[dayIndex % quotes.length];
const funFact = funFacts[dayIndex % funFacts.length];
const readmePath = new URL("../../README.md", import.meta.url);
const readme = await readFile(readmePath, "utf8");

function replaceMarkedContent(content, startMarker, endMarker, replacement) {
  const startIndex = content.indexOf(startMarker);
  const endIndex = content.indexOf(endMarker);

  if (startIndex === -1 || endIndex === -1 || endIndex < startIndex) {
    throw new Error(`Missing or invalid markers: ${startMarker} ... ${endMarker}`);
  }

  const contentStart = startIndex + startMarker.length;
  return `${content.slice(0, contentStart)}\n${replacement}\n${content.slice(endIndex)}`;
}

const withQuote = replaceMarkedContent(
  readme,
  "<!-- DAILY_QUOTE_START -->",
  "<!-- DAILY_QUOTE_END -->",
  `> *"${quote}"* — ${author}`,
);
const updatedReadme = replaceMarkedContent(
  withQuote,
  "<!-- DAILY_FACT_START -->",
  "<!-- DAILY_FACT_END -->",
  `> ${funFact}`,
);

await writeFile(readmePath, updatedReadme);
