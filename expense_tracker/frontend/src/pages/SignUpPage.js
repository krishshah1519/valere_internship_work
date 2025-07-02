import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import api from '../utils/axios';
import { useState } from "react";

export default function SignUpPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [apiError, setApiError] = useState("");
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const response = await api.post("register/", {
        username: data.username,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
        dob: data.dob,
        gender: data.gender,
        phone_number: data.phone_number,
        password: data.password,
        password2: data.password2
      });

      if (response.status === 200 && response.data['otp_token']) {
        navigate('/VerifyOtp', { state: { otp_token: response.data['otp_token'] } });
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


  const inputClasses = "w-full px-4 py-2 mb-3 rounded border border-gray-400 !text-black focus:outline-none focus:ring-2 focus:ring-blue-500";

  return (
    <form
      className="max-w-md mx-auto mt-10 p-8 bg-white  shadow-lg rounded-lg  border border-gray-350 flex flex-col gap-4"
      onSubmit={handleSubmit(onSubmit)}
    >
      {apiError && <p className="text-red-500 text-sm" >{apiError}</p>}

      <input
        placeholder="Username"
        {...register("username", { required: true, maxLength: 20 })}
        className={inputClasses}
      />
      {errors.username && <p className="text-red-500 text-sm">Username is required</p>}

      <input
        type="email"
        placeholder="Email"
        {...register("email", { required: true })}
        className={inputClasses}
      />
      {errors.email && <p className="text-red-500 text-sm">Email is required</p>}

      <input
        type="password"
        placeholder="Password"
        {...register("password", { required: true })}
        className={inputClasses}
      />
      {errors.password && <p className="text-red-500 text-sm">Password is required</p>}

      <input
        type="password"
        placeholder="Confirm Password"
        {...register("password2", { required: true })}
        className={inputClasses}
      />
      {errors.password2 && <p className="text-red-500 text-sm">Confirmation is required</p>}

      <input
        placeholder="First Name"
        {...register("first_name", { required: true })}
        className={inputClasses}
      />
      {errors.first_name && <p className="text-red-500 text-sm">First Name is required</p>}

      <input
        placeholder="Last Name"
        {...register("last_name", { required: true })}
        className={inputClasses}
      />
      {errors.last_name && <p className="text-red-500 text-sm">Last Name is required</p>}

      <input
        type="date"
        {...register("dob", { required: true })}
        className={inputClasses}
      />
      {errors.dob && <p className="text-red-500 text-sm">Date of Birth is required</p>}

      <select {...register("gender", { required: true })} className={inputClasses}>
        <option value="">Select Gender</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
      </select>
      {errors.gender && <p className="text-red-500 text-sm">Gender is required</p>}

      <input
        placeholder="Phone Number"
        {...register("phone_number", { required: true })}
        className={inputClasses}
      />
      {errors.phone_number && <p className="text-red-500 text-sm">Phone Number is required</p>}

      <input
        className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded cursor-pointer transition"
        type="submit"
        value="Sign Up"
      />

      <div className="text-center text-sm mt-2 text-gray-700">
        Already have an account?{" "}
        <span
          onClick={() => navigate('/login')}
          className="text-blue-600 hover:underline cursor-pointer"
        >
          Log In
        </span>
      </div>
    </form>
  );
}
