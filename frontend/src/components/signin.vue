<template>
        <form action="http://127.0.0.1:8000/auth/login" method="POST">
        <label for="username">username</label><input v-model="username" type="text"><br>
        <label for="username">password</label><input v-model="password" type="text"><br>
        <button id="submit" type="submit">submit</button>
    </form>
</template>

<script>
export default {
    props: ['f_signin'],
    data () {
        return {
            username: null,
            password: null,
            login: true,
            signin: true
        }
    },
    mounted () {
        self = this
        document.querySelector('#submit').addEventListener('click', function (e) {
            e.preventDefault()
            self.$http.post('http://127.0.0.1:8500/auth/login', {
                username: self.username,
                password: self.password
            }).then(data => {
                console.log(data)
                console.log('prevented')
                if(data.body.id !== undefined) {
                    self.login = false
                    self.signin = false
                    self.f_signin(false,false,false,data.body.key)
                } else {
                    alert('invalid credentials')
                }
            })
        })
    }
}
</script>

<style>

</style>
