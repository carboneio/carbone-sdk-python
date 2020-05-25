const fs = require("fs");
const path = require("path")
const crypto = require("crypto");

function generateHash(filepath, payload) {
  templateBuffer = fs.readFileSync(path.join(__dirname, filepath));
  return crypto
  .createHash("sha256")
  .update(new Buffer.from(payload))
  .update(templateBuffer)
  .digest("hex");
}

const array_of_hash_generation_test = [
  function testGenerateTemplateId1(index) {
    console.log(`Test${index}: `, generateHash("template.test.odt", ""));
  },
  function testGenerateTemplateId2(index) {
    console.log(`Test${index}: `, generateHash("template.test.odt", "ThisIsAPayload"));
  },
  function testGenerateTemplateId3(index) {
    console.log(`Test${index}: `, generateHash("template.test.odt", "8B5PmafbjdRqHuksjHNw83mvPiGj7WTE"));
  },
  function testGenerateTemplateId4(index) {
    console.log(`Test${index}: `, generateHash("template.test.html", ""));
  },
  function testGenerateTemplateId5(index) {
    console.log(`Test${index}: `, generateHash("template.test.html", "This is a long payload with different characters 1 *5 &*9 %$ 3%&@9 @(( 3992288282 29299 9299929"));
  }
]


array_of_hash_generation_test.forEach((fct, index) => {
  fct(index + 1)
})