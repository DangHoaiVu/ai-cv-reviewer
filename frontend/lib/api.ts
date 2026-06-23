export type ReviewResult = {
  score: number;
  strengths: string[];
  weaknesses: string[];
  missingSkills: string[];
  suggestions: string[];
  suitableRoles: string[];
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

async function parseResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(typeof data.detail === "string" ? data.detail : "Đã có lỗi xảy ra. Vui lòng thử lại.");
  }
  return data as T;
}

export async function uploadAndReview(file: File): Promise<ReviewResult> {
  const form = new FormData();
  form.append("file", file);
  const upload = await fetch(`${API_URL}/api/upload`, { method: "POST", body: form });
  const { fileId } = await parseResponse<{ fileId: string }>(upload);
  const review = await fetch(`${API_URL}/api/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fileId }),
  });
  return parseResponse<ReviewResult>(review);
}
