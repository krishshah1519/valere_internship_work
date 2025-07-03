import { useForm } from "react-hook-form";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../utils/axios";

export default function VerifyOtp() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const navigate = useNavigate();
  const location = useLocation();

  const otp_token = location.state?.otp_token;

  const onSubmit = async (data) => {
    try {
      const res = await api.post(
        "/verify_otp/",
        { otp: data.otp, otp_token },
        { withCredentials: true }
      );
      if (res.status === 201) {
        console.log("Registration successful");
        navigate("/login");
      }
    } catch (err) {
      console.error("Verification failed:", err.response?.data || err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center">Verify OTP</h2>

        <input
          type="number"
          placeholder="Enter 6-digit OTP"
          className="w-full px-4 py-2 border border-gray-300 rounded-md mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          {...register("otp", {
            required: "OTP is required",
            minLength: {
              value: 6,
              message: "OTP must be 6 digits",
            },
            maxLength: {
              value: 6,
              message: "OTP must be 6 digits",
            },
          })}
        />
        {errors.otp && (
          <p className="text-red-500 text-sm mb-4">{errors.otp.message}</p>
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
        >
          Verify
        </button>
      </form>
    </div>
  );
}
