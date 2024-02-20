<template>
    <div class="signup-card">
        <v-card class="mx-auto pa-12 pb-8" elevation="8" rounded="lg" style="margin-bottom: 10vh;">
            <div class="text-h5 text-center mb-8">Sign Up</div>
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
                <v-radio label="Recipient" value="1" color="red"></v-radio>
                <v-radio label="Donor" value="2" color="red"></v-radio>
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
        </v-card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            confirmPassword: '',
            visibleConfirm: false,
            role: '1',
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
            alert('Form Submitted');
            // submission logic here
            this.$router.push({ name: 'login' })
        },
        /**
         * Routes to the sign in page
         */
        goToSignIn() {
            this.$router.push({ name: 'login' });
        },
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
</style>