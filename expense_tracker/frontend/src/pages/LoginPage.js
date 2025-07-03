import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import api from '../utils/axios';
import { useState } from "react";

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [apiError, setApiError] = useState("");
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      await api.get('/csrf/');
      const response = await api.post("/login/", {
        username: data.username,
        password: data.password
      }, { withCredentials: true });

      if (response.status === 200 && response.data.status) {
        console.log("Login successful");


        const isStaff = response.data.is_staff;
        if (isStaff) {
          navigate('/admin-dashboard');

        } else {
          navigate('/home/');
        }
        window.location.reload();
      }
    } catch (error) {
      if (error.response) {
        const data = error.response.data;
        if (data.message) {
          setApiError(data.message);
        } else if (data.error) {
          const fieldErrors = Object.values(data.error).flat().join(" ");
          setApiError(fieldErrors);
        }
      } else {
        setApiError("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-md p-8 rounded-lg shadow-lg border-1 border-lg bg-white"
        autoComplete="off"
      >
        <h2 className="text-3xl font-semibold text-center mb-6 text-gray-800">Login</h2>

        <div>
          <input
            placeholder="Username"
            {...register("username", { required: true, minLength: 4, maxLength: 20 })}
            className="w-full px-4 py-2 mb-3 rounded border border-gray-300 text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.username?.type === "required" && (
            <p className="text-red-500 text-sm mb-2">Username is required</p>
          )}
        </div>

        <div>
          <input
            type="password"
            placeholder="Password"
            {...register("password", { required: true, minLength: 8 })}
            className="w-full px-4 py-2 mb-3 rounded border border-gray-300 text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.password?.type === 'required' && (
            <p className="text-red-500 text-sm mb-2">Password is required</p>
          )}
          {errors.password?.type === 'minLength' && (
            <p className="text-red-500 text-sm mb-2">Password must be at least 8 characters</p>
          )}
        </div>

        {apiError && (
          <p className="text-red-500 text-sm mb-4 text-center">{apiError}</p>
        )}

        <button
          type="submit"
          className="w-full py-2 mt-4 rounded bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors"
        >
          Login
        </button>

        <p className="text-center text-sm mt-4 text-gray-600">
          Don’t have an account?{" "}
          <span
            className="text-blue-600 hover:underline cursor-pointer"
            onClick={() => navigate('/signup')}
          >
            Sign Up
          </span>
        </p>
      </form>
    </div>
  );
}
