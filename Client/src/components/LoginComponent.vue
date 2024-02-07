<script>
import '@mdi/font/css/materialdesignicons.css'
import { user } from '../stores/user.js'
const userData = user()
export default {
    data: () => ({
        visible: false,
        username: '',
        password: '',
        alertText: 'This is a warning alert',
        alert: false,
    }),
    methods: {
        /**
         * Routes to the signup page
         */
        goToSignUp() {
            this.$router.push({ name: 'signup' });
        },
        /**
         * Logs the user in
         */
        login() {
            if (this.username != '' && this.password != '') {
                if (userData.getLoginAttempts >= 3 && this.minutesBetweenDatesVal(userData.getLastLoginAttemptTime) >= 1){
                    this.alertText = `You have exceeded the maximum number of login attempts. Please try again in ${this.minutesBetweenDates(userData.getLastLoginAttemptTime)}`;
                    this.alert = true;
                    return;
                }
                else {
                    if(userData.getLoginAttempts >= 3){
                        userData.resetLoginAttempts()
                    }
                    //LOGIN ATTEMPT HERE

                    userData.setLoginAttempt()
                    //Do API call to check if username and password are correct
                    //If they are correct route to home page and store user token in local storage

                    //IF CORRECT
                    // userData.setLogin(this.username.toLowerCase(), "TOKEN HERE")
                    // userData.resetLoginAttempts()
                    // this.$router.push({ name: 'home' });

                    //else display error message and count failed attempts
                    this.alertText = `Invalid username or password.`;
                    this.alert = true;
                    return;
                }

            } else {
                this.alertText = 'Please enter a username and password';
                this.alert = true;
            }
        },
        /**
         * Routes to the forgot password page
         */
        forgotPass() {
            console.log('Forgot password');
            //Router push to somewhere to reset password
        },
        /**
         * Calculates the minutes between the current time and the input date and returns a stringified version of the minutes or seconds
         * @param {Date} inputDateString 
         */
        minutesBetweenDates(inputDateString) {
            const inputDate = new Date(inputDateString);
            const tenMinutesLater = new Date(inputDate.getTime() + 10 * 60000);
            const now = new Date();
            const diffInMilliseconds = tenMinutesLater.getTime() - now.getTime();
            if (diffInMilliseconds < 60000) {
                return Math.floor(diffInMilliseconds / 1000) + " seconds remaining";
            } else {
                return Math.floor(diffInMilliseconds / 60000) + " minutes remaining";
            }
        },
        /**
         * Calculates the minutes between the current time and the input date
         * @param {Date} inputDateString 
         */
        minutesBetweenDatesVal(inputDateString) {
            const inputDate = new Date(inputDateString);
            const tenMinutesLater = new Date(inputDate.getTime() + 10 * 60000);
            const now = new Date();
            const diffInMilliseconds = tenMinutesLater.getTime() - now.getTime();
            return diffInMilliseconds;
        }
    },
};
</script>

<template>
    <div class="login-card">
        <v-card class="mx-auto pa-12 pb-8" id="card" elevation="8" rounded="lg" style="margin-bottom: 10vh;">
            <div class="text-h5 text-center mb-8">Login</div>
            <v-alert v-model="alert" density="compact" variant="outlined" type="warning" :text="alertText"
                dismissible><v-icon icon="mdi-close" style="float:right"
                    @click="this.alert = false"></v-icon></v-alert>
            <div class="text-subtitle-1 text-medium-emphasis">Account</div>
            <v-text-field density="compact" v-model="username" maxLength="15" placeholder="Username"
                prepend-inner-icon="mdi-account-circle" variant="outlined"></v-text-field>
            <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                Password
                <a class="text-caption text-decoration-none" style="color:#313638; cursor: pointer;" @click="forgotPass">
                    Forgot login password?</a>
            </div>
            <v-text-field :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'" :type="visible ? 'text' : 'password'"
                density="compact" v-model="password" placeholder="Enter your password" maxLength="15"
                prepend-inner-icon="mdi-lock-outline" variant="outlined"
                @click:append-inner="visible = !visible"></v-text-field>
            <v-card class="mb-12" color="#313638" variant="tonal">
                <v-card-text class="text-medium-emphasis text-caption">
                    Warning: After 3 consecutive failed login attempts, you account will be temporarily locked for 10
                    minutes. If you must login now, you can also click "Forgot login password?" above to reset the login
                    password.
                </v-card-text>
            </v-card>
            <v-btn block class="mb-8" color="#F06543" size="large" variant="tonal" @click="login">
                Log In
            </v-btn>
            <v-card-text class="text-center">
                <a class="text-decoration-none" style="color:#313638; cursor: pointer;" @click="goToSignUp">
                    Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
                </a>
            </v-card-text>
        </v-card>
    </div>
</template>

<style scoped>
#card {
    width: 35em;
}
</style>
