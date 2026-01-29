// 登录认证工具类

// 检查用户是否登录并返回token
export function checkLogin() {
  return localStorage.user_token || sessionStorage.user_token;
}

// 获取用户名
export function getUsername() {
  return localStorage.user_name || sessionStorage.user_name;
}

// 获取用户ID
export function getUserId() {
  return localStorage.user_id || sessionStorage.user_id;
}

// 保存登录状态
export function saveLoginStatus(token, userId, username, remember = false) {
  if (remember) {
    // 记住登录状态
    localStorage.user_token = token;
    localStorage.user_id = userId;
    localStorage.user_name = username;
    // 清除sessionStorage中的数据，避免冲突
    sessionStorage.removeItem('user_token');
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('user_name');
  } else {
    // 不记住登录状态
    sessionStorage.user_token = token;
    sessionStorage.user_id = userId;
    sessionStorage.user_name = username;
    // 清除localStorage中的数据，避免冲突
    localStorage.removeItem('user_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
  }
}

// 清除登录状态
export function clearLoginStatus() {
  localStorage.removeItem('user_token');
  localStorage.removeItem('user_id');
  localStorage.removeItem('user_name');
  sessionStorage.removeItem('user_token');
  sessionStorage.removeItem('user_id');
  sessionStorage.removeItem('user_name');
}

// 保存跳转路径
export function saveRedirectPath(path) {
  localStorage.setItem('redirectAfterLogin', path);
}

// 处理未登录情况，显示提示并跳转登录页面
export function handleNotLogin(vm, showConfirm = true) {
  if (showConfirm) {
    return vm.$confirm("对不起，您尚未登录！", "宁夏气象灾害风险识别预测预警系统", {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      // 保存当前路径，以便登录后跳转回来
      saveRedirectPath(vm.$route.fullPath);
      vm.$router.push("/user/login");
    }).catch(() => {
      // 用户点击取消，跳转到首页
      vm.$router.push("/");
    });
  } else {
    // 直接跳转登录页面
    saveRedirectPath(vm.$route.fullPath);
    vm.$router.push("/user/login");
    return Promise.resolve();
  }
}

// 处理登录过期
export function handleLoginExpired(vm, message = "未登录或者登录已过期，请重新登陆") {
  vm.$message.error(message);
  // 保存当前路径，以便登录后跳转回来
  saveRedirectPath(vm.$route.fullPath);
  vm.$router.push("/user/login");
}

// 处理登录后跳转
export function handleLoginRedirect(vm, defaultPath = '/') {
  // 检查是否有保存的跳转路径
  const redirectPath = localStorage.getItem('redirectAfterLogin');
  if (redirectPath) {
    // 清除保存的路径
    localStorage.removeItem('redirectAfterLogin');
    // 跳转到原页面
    vm.$router.push(redirectPath);
  } else {
    // 默认跳转到首页
    vm.$router.push(defaultPath);
  }
}
