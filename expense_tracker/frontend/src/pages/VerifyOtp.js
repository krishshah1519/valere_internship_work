import {useForm} from "react-hook-form";
import {useNavigate} from "react-router-dom";
import api from '../utils/axios'
import {useLocation} from "react-router-dom";

export default function VerifyOtp(){
    const{register, handleSubmit, formState:{errors}
    } = useForm();
    const navigate = useNavigate()
    const location = useLocation();

    const otp_token = location.state?.otp_token;

    const onSubmit = async (data)=> {

        await api.post("/verify_otp/",{"otp":data.otp,"otp_token":otp_token}, {withCredentials: true}).then(res =>{
            if (res.status === 201 ){
            console.log("Registration successful");
            navigate('/login');
        }
        })
    }

    return(
        <form onSubmit={handleSubmit(onSubmit)}>
            <input placeholder={"enter otp"} type={"number"} {...register("otp", {required: true, minLength:6,maxLength:6}) }/>

            <input type={"submit"}/>
        </form>
    )
}
