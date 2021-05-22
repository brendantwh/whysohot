const switchToggle = document.querySelector("#switch-toggle");
const switchToggleBG = document.querySelector("#switch-toggle-bg");
const mobileToggle = document.querySelector("#mobile-toggle")
const iconDarkMobile = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />';
const iconLightMobile = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />';      
var theme = localStorage.theme;

function dropdown() {
    return {
        selected: [],
        add(num) { this.selected.push(num) },
        rem(num) { index = this.selected.indexOf(num); this.selected.splice(index, 1); },
        allAdd() { 
            for (var i = 1; i <= s_no.length; i++) {
                if (this.selected.includes(i) != true) {
                    this.selected.push(i);
                }
            }
        },
        allRem() { this.selected = []; },
        check() {
            if (window.matchMedia("(min-width: 768px)").matches) {
                this.allAdd();
            }
        },
    }
};

function toggleTheme() {
    if (theme == 'light') {
        switchToggle.classList.add('translate-x-7');
        switchToggleBG.classList.add('bg-dark-200');
        mobileToggle.innerHTML = iconDarkMobile;
        setTimeout(() => {
            document.documentElement.classList.add('dark');
        }, 100);
        theme = 'dark';
    } 
    else {
        switchToggle.classList.remove('translate-x-7');
        switchToggleBG.classList.remove('bg-dark-200');
        mobileToggle.innerHTML = iconLightMobile;
        setTimeout(() => {
            document.documentElement.classList.remove('dark');
        }, 100);
        theme = 'light';
    }
};

if (window.matchMedia('(prefers-color-scheme: dark)').matches)
{
    theme = 'light';
    toggleTheme();
} 