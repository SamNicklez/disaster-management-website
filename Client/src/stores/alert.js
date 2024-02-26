// alert.js
import { reactive } from 'vue';

export const alertStore = reactive({
    display: true,
    text: 'This is a test message.',
    type: 'warning',
    title: 'Test'
});

