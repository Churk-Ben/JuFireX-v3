import http from "@/utils/request";

export interface HelloResponse {
	message: string;
}

export async function getHelloStatus(): Promise<HelloResponse> {
	return await http.get("/api/hello");
}
