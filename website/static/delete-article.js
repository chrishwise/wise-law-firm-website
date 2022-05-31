function deleteArticle(articleId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ articleId: articleId }),
  }).then((_res) => {
    window.location.href = "/articles";
  });
}