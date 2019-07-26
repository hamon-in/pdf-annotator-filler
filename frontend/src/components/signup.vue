<template>
    <form action="http://127.0.0.1:8000/auth/register" method="POST">
        <label for="e-mail">e-mail</label><input v-model="email" type="text"><br>
        <label for="username">username</label><input v-model="username" type="text"><br>
        <label for="password">password</label><input v-model="password" type="text"><br>
        <button id='submit' type="submit">submit</button>
    </form>
</template>

<script>

export default {
    props: ['f_signin'],
    data () {
        return {
            email: null,
            username: null,
            password: null,
            login: true,
            signup: true
        }
    },
    mounted () {
        self = this
        document.querySelector('#submit').addEventListener('click',async function (e) {
            e.preventDefault()
            await self.$http.post('http://127.0.0.1:8500/auth/register', {
                email: self.email,
                username: self.username,
                password: self.password
            }).then(data => {
                console.log(data)
                console.log('prevented')
                if(Object.entries(data.body).length === 1) {
                    self.login = false
                    self.signup = false
                    console.log(self.login)
                } else {
                    alert('invalid entry')
                }
            })
            if(!self.login) {
                self.$http.post('http://127.0.0.1:8000/auth/login', {
                    username: self.username,
                    password: self.password
                }).then(data => {
                    console.log(data)
                    console.log('prevented')
                    self.f_signin(false,false,false,data.body.key)
                })
            }
        })

    }
}
</script>

<style>

</style>
