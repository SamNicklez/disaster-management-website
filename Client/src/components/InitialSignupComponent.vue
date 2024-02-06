<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            usernameRules: [
                v => !!v || 'Username is required',
                v => (v && v.length >= 8 && v.length <= 15) || 'Username must be 8-15 characters long',
                v => /^[a-zA-Z0-9]*$/.test(v) || 'Username must be alphanumeric',
            ],
            passwordRules: [
                v => !!v || 'Password is required',
            ],
            passwordRequirements: [
                { rule: 'Must have 8-15 characters', valid: false },
                { rule: 'Must contain valid characters', valid: false },
                { rule: 'At least 1 special character (ex: . , ? ! )', valid: false },
            ],
        };
    },
    computed: {
        valid() {
            const usernameValid = this.usernameRules.slice(0, -1).every(rule => rule(this.username) === true);
            const passwordValid = this.passwordRequirements.every(req => req.valid);
            return usernameValid && passwordValid;
        }
    },
    methods: {
        validatePassword() {
            const hasLength = this.password.length >= 8 && this.password.length <= 15;
            const hasSpecialChar = /[,.?!]/.test(this.password);
            const isValidCharacters = /^[a-zA-Z0-9,.?!]+$/.test(this.password);

            this.passwordRequirements[0].valid = hasLength;
            this.passwordRequirements[1].valid = isValidCharacters;
            this.passwordRequirements[2].valid = hasSpecialChar;
        },
        submit() {
            alert('Form Submitted');
            // submission logic here
        },
    },
};
</script>


<template>
    <v-card title="Login" class="mx-auto pa-12 pb-8" id="card" elevation="8" rounded="lg" style="margin-bottom: 10vh;">
        <v-container>
            <v-form class="form" ref="form" v-model="valid" lazy-validation>
                <v-text-field label="Username" v-model="username" :rules="[usernameRules]" required></v-text-field>

                <v-text-field label="Password" v-model="password" :type="'password'" :rules="[passwordRules]" required
                    @input="validatePassword"></v-text-field>

                <v-card class="mb-12" color="#313638" variant="tonal">
                    <v-list density="compact">
                        <v-list-subheader>Password Requirements</v-list-subheader>

                        <v-list-item v-for="(item, index) in passwordRequirements" :key="index">
                            <template v-slot:append v-if="item.valid">
                                <v-icon color="green" icon="mdi-check-circle"></v-icon>
                            </template>
                            <v-list-item-title>{{ item.rule }}</v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-card>

                <v-btn :disabled="!valid" color="primary" @click="submit">Sign Up</v-btn>
            </v-form>
        </v-container>
    </v-card>
</template>

<style scoped>
#card {
    max-width: 30%;
}
</style>