<template>
        <form action="http://0.0.0.0:8000/auth/login" method="POST">
        <label for="username">username:</label><input v-model="username" type="text" placeholder='username'><br>
        <label for="username">password:</label><input v-model="password" type="text" placeholder='password'><br>
        <input class='btn' id="submit" type="submit" value='submit'>
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
            self.$http.post('http://0.0.0.0:8500/auth/login', {
                username: self.username,
                password: self.password
            }).then(data => {
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

form {
        border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
    }

</style>
