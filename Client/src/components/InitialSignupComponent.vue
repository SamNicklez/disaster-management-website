<template>
    <v-dialog v-model="dialog" width="auto" persistent>
        <v-card>
            <v-alert v-model="alert2" class="alert" density="compact" type="warning" :title="alertText2"
                variant="tonal"></v-alert>
            <v-card-text>
                Account created!
                An email has been sent to your email address, please enter the code to verify your account.
            </v-card-text>
            <v-text-field variant="outlined" label="Verification Code" v-model="verifyCode" required dense outlined
                placeholder="Enter verification code" maxLength="6"
                style="min-width: 50%; margin: auto; margin-top: 2.5vh;">
            </v-text-field>
            <v-card-actions>
                <v-btn color="primary" block @click="verify()">Submit</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <div class="signup-card">
        <v-card class="mx-auto pa-12 pb-8" elevation="8" rounded="lg" style="margin-bottom: 10vh;">
            <div class="text-h5 text-center mb-8">Sign Up</div>
            <v-alert v-model="alert" class="alert" density="compact" type="warning" title="Warning" variant="tonal"
                :text="alertText"></v-alert>
            <v-text-field data-test="username-input" class="textfield" variant="outlined" label="Email" v-model="username"
                :rules="usernameRules" required dense outlined placeholder="Enter your email address"
                prepend-inner-icon="mdi-account-circle" maxLength="100">
            </v-text-field>
            <v-text-field data-test="password-input" class="textfield" variant="outlined" label="Password"
                v-model="password" :rules="passwordRules" required @input="validatePassword" dense outlined
                placeholder="Create a password" prepend-inner-icon="mdi-lock-outline" type="password"
                @click:append-inner="visible = !visible" maxLength="15">
            </v-text-field>
            <v-text-field data-test="confirm-password-input" class="textfield" variant="outlined" label="Confirm Password"
                v-model="confirmPassword" :type="visibleConfirm ? 'text' : 'password'" :rules="confirmPasswordRules"
                required dense outlined placeholder="Confirm your password" prepend-inner-icon="mdi-lock-outline">
            </v-text-field>
            <v-card data-test="password-requirements-card" class="mb-12" color="#F06543" variant="tonal">
                <v-card-title class="text-h6 text-center">Password Requirements</v-card-title>
                <v-list dense>
                    <v-list-item v-for="(item, index) in passwordRequirements" :key="index"
                        :data-test="`password-requirement-${index}`">
                        <template v-slot:append v-if="item.valid">
                            <v-icon color="green" icon="mdi-check-circle"></v-icon>
                        </template>
                        <v-list-item-title>{{ item.rule }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-card>
            <v-radio-group label="Select a Role" v-model="role">
                <v-radio label="Recipient" value="3" color="red"></v-radio>
                <v-radio label="Donor" value="2" color="red"></v-radio>
                <v-radio label="Admin" value="1" color="red"></v-radio>
            </v-radio-group>
            <v-btn data-test="signup-button" :disabled="!valid" block class="mb-8" color="#F06543" size="large"
                variant="tonal" style="" @click="submit">
                Sign Up
            </v-btn>

            <v-card-text class="text-center mt-4">
                <a data-test="signin-link" class="text-decoration-none" style="color:#313638; cursor: pointer;"
                    @click="goToSignIn">
                    Already have an account? Sign in <v-icon right>mdi-chevron-right</v-icon>
                </a>
            </v-card-text>
            <v-progress-linear :active="progress" indeterminate color="orange" height="10" rounded></v-progress-linear>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            alertText: 'Test',
            alertText2: 'Test',
            dialog: false,
            alert: false,
            alert2: false,
            username: '',
            password: '',
            confirmPassword: '',
            visibleConfirm: false,
            verifyCode: '',
            progress: false,
            role: '3',
            usernameRules: [
                v => !!v || 'Email is required',
                v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Email must be a valid email address',
            ],
            passwordRules: [
                v => !!v || 'Password is required',
            ],
            passwordRequirements: [
                { rule: 'Must have 8-15 characters', valid: false },
                { rule: 'Contain valid characters', valid: false },
                { rule: 'Contain at least one captial letter', valid: false },
                { rule: 'Have at least 1 special character (ex: . , ? ! )', valid: false },
            ],
        };
    },
    computed: {
        /**
         * Check if the form is valid
         */
        valid() {
            const usernameValid = this.usernameRules.slice(0, -1).every(rule => rule(this.username) === true);
            const passwordValid = this.passwordRequirements.every(req => req.valid);
            return usernameValid && passwordValid && (this.password === this.confirmPassword);
        },
        /**
         * Confirm password rules
         */
        confirmPasswordRules() {
            return [
                v => !!v || 'Confirm password is required',
                v => v === this.password || 'Passwords must match',
            ];
        }
    },
    methods: {
        /**
         * Validates password
         */
        validatePassword() {
            const hasLength = this.password.length >= 8 && this.password.length <= 15;
            const hasSpecialChar = /[,.?!]/.test(this.password);
            const isValidCharacters = /^[a-zA-Z0-9,.?!]+$/.test(this.password);
            const hasUpperCase = /[A-Z]/.test(this.password);

            this.passwordRequirements[0].valid = hasLength;
            this.passwordRequirements[1].valid = isValidCharacters;
            this.passwordRequirements[2].valid = hasUpperCase;
            this.passwordRequirements[3].valid = hasSpecialChar;
        },
        /**
         * Submits the signup form and routes to next part of the signup process
         */
        submit() {
            this.progress = true
            let data = JSON.stringify({
                "email": this.username.toLowerCase(),
                "password": this.password,
                "roleid": parseInt(this.role)
            });

            let config = {
                method: 'post',
                maxBodyLength: Infinity,
                url: 'http://127.0.0.1:5000/users_bp/signup',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: data
            };

            axios.request(config)
                .catch((error) => {
                    this.progress = false
                    if (error.response.status === 409) {
                        this.alertText = "Account with that email already exists";
                    }
                    else if (error.response.status === 500) {
                        this.alertText = "Internal server error";
                    }
                    else {
                        this.alertText = "An error occurred";
                    }
                    this.alert = true;
                    window.scrollTo(0, 0);
                }).then((response) => {
                    if (response) {
                        // this.dialog = true
                        this.progress = false
                        this.$router.push({ name: 'home' });
                    }
                })

        },
        /**
         * Routes to the sign in page
         */
        goToSignIn() {
            this.$router.push({ name: 'login' });
        },
        /**
         * Verifies the code
         */
        verify() {
            let data = JSON.stringify({
                "email": this.username.toLowerCase(),
                "verification": this.verifyCode
            });

            let config = {
                method: 'post',
                maxBodyLength: Infinity,
                url: 'http://127.0.0.1:5000/users_bp/verify',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: data
            };

            axios.request(config)
                .then(() => {
                    this.$router.push({ name: 'login' });
                })
                .catch((error) => {
                    if (error.response.status === 401) {
                        this.alertText2 = "Invalid verification code";
                    }
                    else if (error.response.status === 500) {
                        this.alertText2 = "Internal server error";
                    }
                    else {
                        this.alertText2 = "An error occurred";
                    }
                    this.alert2 = true;
                });
        }
    },
};
</script>


<style scoped>
.signup-card {
    max-width: 35em;
    margin: auto;
}

.text-caption {
    color: #FFF;
}

.textfield {
    margin-bottom: 1.5vh;
}

.alert {
    margin-bottom: 3vh;
}
</style>