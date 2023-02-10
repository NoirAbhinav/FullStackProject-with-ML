import axios from "axios";
async function ApiOnClick(endpoint, user_id) {
  const response = await axios.post(
    "http://localhost:8000/" + endpoint,
    {
      ml_module: "emotions",
      user_id: user_id,
    },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  return response.data;
}
export default ApiOnClick;
