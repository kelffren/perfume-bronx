import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from './config.js';
const API = SUPABASE_URL + '/auth/v1';
const headers = {'apikey':SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'};
const storageKey='oud-bronx-customer-session';
let session=null;
try { session=JSON.parse(localStorage.getItem(storageKey)||'null'); } catch { localStorage.removeItem(storageKey); }
function save(data) {
 if(data?.access_token && data?.refresh_token) {
  session={access_token:data.access_token,refresh_token:data.refresh_token,expires_at:Math.floor(Date.now()/1000)+(data.expires_in||3600),user:data.user};
  localStorage.setItem(storageKey,JSON.stringify(session));
 }
}
async function request(path,body,token) {
 const response=await fetch(API+path,{method:'POST',headers:{...headers,...(token?{Authorization:'Bearer '+token}:{})},body:JSON.stringify(body)});
 const data=await response.json().catch(()=>({}));
 if(!response.ok)throw new Error(data.msg||data.error_description||data.message||data.error||'Authentication failed');
 return data;
}
export async function signup(email,password,redirect) {
 return request('/signup?redirect_to='+encodeURIComponent(redirect),{email,password});
}
export async function login(email,password) {
 const result=await request('/token?grant_type=password',{email,password});save(result);return result;
}
export async function resetPassword(email,redirect) {
 return request('/recover?redirect_to='+encodeURIComponent(redirect),{email});
}
export async function currentUser() {
 if(!session?.access_token)return null;
 if(session.expires_at < Date.now()/1000+60) {
  try {const data=await request('/token?grant_type=refresh_token',{refresh_token:session.refresh_token});save(data);}
  catch {session=null;localStorage.removeItem(storageKey);return null;}
 }
 const response=await fetch(API+'/user',{headers:{apikey:SUPABASE_PUBLISHABLE_KEY,Authorization:'Bearer '+session.access_token}});
 if(!response.ok){session=null;localStorage.removeItem(storageKey);return null;}
 return response.json();
}
export async function logout() {
 if(session?.access_token)await request('/logout',{},session.access_token).catch(()=>{});
 session=null;localStorage.removeItem(storageKey);
}
