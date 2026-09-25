const API_BASE = import.meta.env.VITE_API_BASE ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const msg =
      body?.error?.message || body?.detail || `Request failed (${res.status})`;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return res.json() as Promise<T>;
}

export type MessageIntakeResponse = {
  conversation_id: string;
  message_id: string;
  lead_id?: string | null;
  response: string;
  qualification_level?: string | null;
  urgency?: string | null;
};

export type ChatMessage = {
  id: string;
  conversation_id: string;
  sender_type: string;
  content: string;
  created_at: string;
};

export type Lead = {
  id: string;
  customer_id: string;
  status: string;
  intent: string;
  property_type: string;
  location_text?: string | null;
  bedrooms?: number | null;
  budget_min?: string | null;
  budget_max?: string | null;
  currency: string;
  timeframe: string;
  qualification_level: string;
  qualification_score?: number | null;
  urgency: string;
  notes?: string | null;
  created_at: string;
  updated_at: string;
  customer_name?: string | null;
  customer_email?: string | null;
  customer_phone?: string | null;
};

export type LeadListResponse = {
  items: Lead[];
  total: number;
  page: number;
  limit: number;
};

export async function sendMessage(body: {
  message: string;
  conversation_id?: string | null;
  customer_name?: string;
  customer_phone?: string;
}): Promise<MessageIntakeResponse> {
  return request<MessageIntakeResponse>("/api/messages", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function getConversationMessages(
  conversationId: string
): Promise<ChatMessage[]> {
  return request<ChatMessage[]>(`/api/conversations/${conversationId}/messages`);
}

export async function listLeads(params?: {
  page?: number;
  limit?: number;
  status?: string;
  qualification?: string;
  urgency?: string;
}): Promise<LeadListResponse> {
  const q = new URLSearchParams();
  if (params?.page) q.set("page", String(params.page));
  if (params?.limit) q.set("limit", String(params.limit));
  if (params?.status) q.set("status", params.status);
  if (params?.qualification) q.set("qualification", params.qualification);
  if (params?.urgency) q.set("urgency", params.urgency);
  const qs = q.toString();
  return request<LeadListResponse>(`/api/leads${qs ? `?${qs}` : ""}`);
}

export async function getLead(id: string): Promise<Lead> {
  return request<Lead>(`/api/leads/${id}`);
}

export async function updateLeadStatus(
  id: string,
  status: string,
  reason?: string
): Promise<Lead> {
  return request<Lead>(`/api/leads/${id}/status`, {
    method: "POST",
    body: JSON.stringify({ status, reason }),
  });
}
