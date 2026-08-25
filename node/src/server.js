import express from "express";
import { fastapi } from "./fastapi.js";

const app = express();

app.use(express.json());

app.get("/api/data", async (req, res) => {
  const result = await fastapi("/api/data");

  res
    .status(result.status)
    .json(result.data);
});

/*
app.post("/api/users", async (req, res) => {
  const result = await fastapi(
    "/api/users",
    {
      method: "POST",
      body: req.body
    }
  );

  res
    .status(result.status)
    .json(result.data);
});
*/
app.listen(4000)