<template>
    <form action="http://127.0.0.1:8000/auth/register" method="POST">
        <label for="e-mail">e-mail</label><input type="text"><br>
        <label for="username">username</label><input type="text"><br>
        <label for="password">password</label><input type="text"><br>
        <button id='submit' type="submit">submit</button>
        Document.getElementByid('submit').addEventListener('click', function (e) {
            e.preventDefault()
        })
    </form>
</template>

<script>
export default {

}
</script>

<style>

</style>
