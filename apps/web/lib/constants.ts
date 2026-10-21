// Matches the max_length constraint on AskRequest.question in the API.
export const MAX_QUESTION_LENGTH = 1000;

export const KNOWLEDGE_SOURCE = {
  publisher: "WHO",
  title: "Diabetes monitoring guidance",
} as const;

export const SUGGESTED_QUESTIONS: readonly string[] = [
  "Which indicators measure diabetes mortality?",
  "How is diabetes prevalence monitored?",
  "What indicators are used to assess diabetes care?",
  "What are the core indicators in the monitoring framework?",
];
