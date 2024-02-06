<script>
import '@mdi/font/css/materialdesignicons.css'
export default {
    data: () => ({
        visible: false,
        username: '',
        password: '',
    }),
    methods: {
        goToSignUp() {
            this.$router.push({ name: 'signup' });
        },
        login(){
            console.log('Logging in');
            console.log(this.username);
            console.log(this.password);
        },
    },
};
</script>

<template>
    <div>
        <v-card title="Login" class="mx-auto pa-12 pb-8" id="card" elevation="8" rounded="lg" style="margin-bottom: 10vh;">
            <div class="text-subtitle-1 text-medium-emphasis">Account</div>
            <v-text-field density="compact" v-model="username" maxLength="15" placeholder="Username" prepend-inner-icon="mdi-account-circle"
                variant="outlined"></v-text-field>
            <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                Password
                <a class="text-caption text-decoration-none text-blue" href="#" rel="noopener noreferrer" target="_blank">
                    Forgot login password?</a>
            </div>
            <v-text-field :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'" :type="visible ? 'text' : 'password'"
                density="compact" v-model="password" placeholder="Enter your password" maxLength="15" prepend-inner-icon="mdi-lock-outline" variant="outlined"
                @click:append-inner="visible = !visible"></v-text-field>
            <v-card class="mb-12" color="surface-variant" variant="tonal">
                <v-card-text class="text-medium-emphasis text-caption">
                    Warning: After 3 consecutive failed login attempts, you account will be temporarily locked for three
                    hours. If you must login now, you can also click "Forgot login password?" below to reset the login
                    password.
                </v-card-text>
            </v-card>
            <v-btn block class="mb-8" color="blue" size="large" variant="tonal" @click="login">
                Log In
            </v-btn>
            <v-card-text class="text-center">
                <a class="text-blue text-decoration-none" href="#" @click="goToSignUp">
                    Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
                </a>
            </v-card-text>
        </v-card>
    </div>
</template>

<style scoped>
#card{
    max-width: 40%;
}
</style>
