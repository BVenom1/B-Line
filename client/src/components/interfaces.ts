import { ReactNode } from "react";

export interface UserModel {
    user_id?: number,
    user_name?: string,
    email?: string,
    status?: string,
    is_verified?: boolean,
    created_at?: Date,
    verified_at?: Date
}

export interface AlertModel {
    alert_id: string,
    style?: "Message" | "Error" | "Success" | "Info" | "Warning",
    children?: ReactNode,
}

export interface GroupModel {
    group_id?: number,
    group_name?: string,
    description?: string,
    created_at?: Date,
}

export interface MembershipModel {
    membership_id?: number,
    user_id?: number,
    group_id?: number,
    joined_at?: Date,
    membership_type?: "member" | "admin" | "banned" | "left",
    notification_type?: "notify" | "mute"
}