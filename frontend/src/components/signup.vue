<template>
    <form action="http://127.0.0.1:8000/auth/register" method="POST">
        <label for="e-mail">e-mail</label><input v-model="email" type="text"><br>
        <label for="username">username</label><input v-model="username" type="text"><br>
        <label for="password">password</label><input v-model="password" type="text"><br>
        <button id='submit' type="submit">submit</button>
    </form>
</template>

<script>

    // Document.getElementByid('submit').addEventListener('click', function (e) {
    //         e.preventDefault()
    //         this.$http.post('http://127.0.0.1:8000/auth/register', {
    //             username: this.email,
    //             username: this.username,
    //             password: null.password
    //         }).then(data => console.log(data))
    //     })

export default {
    data () {
        return {
            email: null,
            username: null,
            password: null
        }
    }
}
</script>

<style>

</style>
