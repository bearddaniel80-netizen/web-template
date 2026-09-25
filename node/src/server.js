import express from "express";
import cors from "cors";
import { forwardFastapi } from "./middleware/forewardFastapi.js";
import { upload, upload_to_fastapi } from "./utils/fastapi.js";

const app = express();

app.use(express.json());
app.use(cors());

/*
 * ==================================================
 * Dynamic Routes
 * ==================================================
 */

/*
 * ==================================================
 * Static Routes
 * ==================================================
 */
app.get("/api/data",
  forwardFastapi("/api/data")
);


app.post("/api/uploads",   upload.single("file"),
  async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({
          error: "No file uploaded",
        });
      }

      const result = await upload_to_fastapi(
        "/api/uploads",
        req.file,
        {
          description: req.body.description,
        }
      );

      res
        .status(result.status)
        .json(result.data);

    } catch (error) {
      console.error("Upload failed:", error);

      res.status(500).json({
        error: "Upload failed",
      });
    }
  }
);
app.listen(4000, "0.0.0.0", () => {
  console.log("Server listening on port 4000");
});