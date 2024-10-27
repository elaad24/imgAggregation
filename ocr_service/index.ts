const tesseract = require("tesseract.js");
const fs = require("fs");
const path = require("path");

const convert_img_to_txt = async (fileNameArr: string[]) => {
  const dir_files_to_convert = "../imagesFolder/preSort";
  try {
    fs.readdir(dir_files_to_convert, (err, files) => {
      if (err) {
        return console.log("Unable to scan directory:", err);
      }
      files.forEach(async (file) => {
        if (fileNameArr.includes(file)) {
          const filePath = path.join(dir_files_to_convert, file);
          const outputPath = `../classification_service/text_files/${file}.txt`;

          const result = await tesseract.recognize(filePath, "eng", {
            logger: (e) => console.log(e.status, e.progress),
          });
          console.log(result.data.text);
          saveTextToFile(result.data.text, outputPath);
        }
      });
    });
  } catch (err) {
    console.error("Error processing image to text:", err);
  }
};

const saveTextToFile = (text, outputPath) => {
  fs.appendFile(outputPath, text, (err) => {
    if (err) {
      console.error("Error writing to file:", err);
    } else {
      console.log("Text successfully written as", outputPath);
    }
  });
};

const fileNameArr = ["a", "b", "c"];
convert_img_to_txt(fileNameArr);
