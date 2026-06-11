<template>
  <code class="math-expr">{{ expression }}</code>
</template>

<script setup>
defineProps({
  expression: { type: String, required: true },
})
</script>
