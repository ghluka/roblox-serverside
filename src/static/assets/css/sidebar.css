* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    width: 78px;
    background: var(--side);
    border-right: 2px solid var(--border);
    z-index: 1;
    transition: all 0.5s ease;
    overflow-y: auto;
    overflow-x: hidden;
}

@media (max-width: 1053px) {
    .sidebar .logo-details .logo_name {
        padding-left: 12px!important;
        opacity: 1!important;
    }
    .sidebar > .logo-details > .logo_name > span:nth-of-type(2) {
        display: none;
    }
    #btn {
        display: none;
    }

    .sidebar .nav-list {
        padding: 0!important;
        width: 54px;
        transition: transform 0.3s ease;
    }
    
    .sidebar .logo-details #btn {
        left: 0;
    }
    
}

@media (min-width: 1053px) {
    .sidebar.open {
        width: 250px;
    }

    .sidebar.open .logo-details,
    .sidebar.open .logo-details .logo_name {
        opacity: 1;
    }
    
    .sidebar.open .logo-details #btn {
        text-align: center;
    }
    
    .sidebar:not(.open) .nav-list {
        padding: 0!important;
        width: 54px;
        transition: transform 0.3s ease;
    }
    
    .sidebar:not(.open) .logo-details #btn {
        left: 0;
    }
    
    .sidebar.open input {
        padding: 0 20px 0 50px;
        width: 100%;
    }
    
    .sidebar.open .bx-search:hover {
        background: var(--side);
        color: #fff;
    }
    
    .sidebar.open li a .links_name {
        opacity: 1;
        pointer-events: auto;
    }

    .sidebar.open li .tooltip {
        display: none;
    }

    .sidebar.open li.profile {
        width: 250px;
    }
    
    .sidebar.open .profile #log_out {
        width: 50px;
        background: none;
    }
    
    .sidebar.open~.home-section {
        left: 250px;
        width: calc(100% - 250px)!important;
    }
}

.sidebar .logo-details {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
}

.logo_name {
    color: #fff;
    font-size: 100%;
    font-weight: 600;
    cursor: pointer;
}

.sidebar .logo-details .logo_name {
    font-size: 20px!important;
    opacity: 0;
    transition: all 0.5s ease;
    padding-left: 16px;
}

.logo_name * {
    font-family: "Bowlby One SC", sans-serif;
    font-weight: 400;
    font-style: normal;
}

.sidebar .logo-details #btn {
    position: absolute;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    font-size: 22px;
    text-align: center;
    cursor: pointer;
    transition: all 0.5s ease;
}

.sidebar i {
    color: #fff;
    height: 60px;
    min-width: 50px;
    font-size: 28px;
    text-align: center;
    line-height: 60px;
}

.sidebar .nav-list {
    margin-top: 20px;
    margin-right: auto;
    margin-left: auto;
    padding: 0 16px;
}

.sidebar li {
    position: relative;
    margin: 8px 0;
    list-style: none;
}

.sidebar input {
    font-size: 15px;
    color: #fff;
    font-weight: 400;
    outline: none;
    height: 50px;
    width: 100%;
    border: none;
    border-radius: 12px;
    transition: all 0.5s ease;
    background: var(--side);
}

.sidebar .bx-search {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    font-size: 22px;
    background: var(--side);
    color: #fff;
}

.sidebar .bx-search:hover {
    background: #fff;
    color: var(--side);
}

.sidebar li i {
    height: 50px;
    line-height: 50px;
    font-size: 18px;
    border-radius: 12px;
}

.sidebar li a {
    display: flex;
    height: 100%;
    width: 100%;
    border-radius: 12px;
    align-items: center;
    text-decoration: none;
    transition: all 0.4s ease;
    background: var(--side);
    border: var(--side) 2px solid;
}

.sidebar li a:hover {
    background: var(--side);
}

.sidebar li a i {
    color: #606070;
    transition: 0.4s;
}

#tab-selected i {
    color: var(--nett)!important;
}

#tab-selected {
    background-color: var(--selected);
    border: var(--nett) 2px solid;
    box-shadow: 0 0 8px rgba(var(--accent-rgb), 0.3);
    overflow: visible!important;
    color: #fff;
}

#tab-selected * {
    color: #fff;
    z-index: 2;
}

.sidebar li a .links_name {
    color: #606070;
    font-size: 15px;
    font-weight: 400;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: 0.4s;
}

.sidebar li a:hover .links_name {
    transition: all 0.5s ease;
    color: #fff;
}

.ace_gutter {
    z-index: 0!important;
}

.sidebar li .tooltip {
    position: absolute;
    top: -20px;
    left: calc(100% + 15px);
    background: #fff;
    color: #000!important;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 15px;
    font-weight: 400;
    opacity: 0;
    white-space: nowrap;
    pointer-events: none;
    transition: 0s;
}

.sidebar li:hover .tooltip {
    opacity: 1;
    pointer-events: auto;
    transition: all 0.4s ease;
    top: 50%;
    transform: translateY(-50%);
}

.sidebar li.profile {
    position: fixed;
    height: 60px;
    width: 78px;
    left: 0;
    bottom: -8px;
    padding: 10px 14px;
    background: var(--side);
    transition: all 0.5s ease;
    overflow: hidden;
}

.sidebar li .profile-details {
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
}

.sidebar li img {
    height: 45px;
    width: 45px;
    object-fit: contain;
    border-radius: 6px;
    margin-right: 10px;
}

.sidebar li.profile .name,
.sidebar li.profile .job {
    font-size: 15px;
    font-weight: 400;
    color: #fff;
    white-space: nowrap;
}

.sidebar li.profile .job {
    font-size: 12px;
}

.sidebar .profile #log_out {
    position: absolute;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    background: var(--side);
    width: 100%;
    height: 60px;
    line-height: 60px;
    transition: all 0.5s ease;
}

.home-section {
    position: relative;
    min-height: 100svh;
    top: 0;
    left: 78px;
    width: calc(100% - 78px);
    padding: 12px;
    transition: all 0.5s ease;
    display: flex;
    flex-direction: column;
}

.home-section.tab-enter {
    animation: tab-enter 180ms ease-out both;
}

.home-section.tab-enter > div {
    animation: tab-content-enter 220ms ease-out both;
}

@keyframes tab-enter {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes tab-content-enter {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    .home-section.tab-enter,
    .home-section.tab-enter > div {
        animation: none;
    }
}

.home-section > div {
    flex-grow: 1;
}

.home-section .text {
    display: inline-block;
    color: var(--side);
    font-size: 25px;
    font-weight: 500;
    margin: 18px;
}
