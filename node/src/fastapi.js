import { readFileSync } from "fs";

function readSecret(name) {
    const path = `/run/secrets/${name}`;

    try {
        return readFileSync(path, "utf8").trim();
    } catch (err) {
        console.error(`Could not read secret: ${path}`);
        process.exit(1);
    }
}
const FASTAPI_URL = process.env.FASTAPI_URL;
const FASTAPI_INTERNAL_KEY = readSecret("fastapi_internal_key");

export async function fastapi(
  path,
  {
    method = "GET",
    body,
    headers = {}
  } = {}
) {
  const response = await fetch(
    `${FASTAPI_URL}${path}`,
    {
      method,

      headers: {
        "X-Internal-Key": FASTAPI_INTERNAL_KEY,
        "Accept": "application/json",

        ...(body !== undefined
          ? { "Content-Type": "application/json" }
          : {}),

        ...headers
      },

      ...(body !== undefined
        ? { body: JSON.stringify(body) }
        : {})
    }
  );

  let data = null;

  const contentType =
    response.headers.get("content-type");

  if (contentType?.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  return {
    status: response.status,
    ok: response.ok,
    data
  };
}