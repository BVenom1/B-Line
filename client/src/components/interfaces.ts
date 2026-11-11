import { ReactNode } from "react";

export interface UserModel {
    user_id?: Number,
    user_name?: string,
    email?: string,
    status?: string,
    is_verified?: boolean,
    created_at?: Date,
    verified_at?: Date
}

export interface AlertModel {
    alert_id: string,
    style?: "Message" | "Error" | "Success" | "Info",
    children?: ReactNode,
}