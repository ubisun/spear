;; Remove toolbar and menu bar
(tool-bar-mode -1)
(menu-bar-mode -1)
(scroll-bar-mode -1)
(global-linum-mode 1)
(setq linum-format "%d ")
(setq inhibit-startup-screen t)

(setq make-backup-files nil)
(setq auto-save-default nil)

;; Load theme
(add-hook 'after-init-hook (lambda () (load-theme 'darkburn)))

;; proxy
;(setq url-proxy-services
;  '(("no_proxy" . "^\\(localhost\\|10.*\\)")
;    ("http" . "75.12.251.5:8080")))

(require 'package)
(add-to-list 'package-archives
	     '("melpa" . "http://melpa.milkbox.net/packages/") t)

(package-initialize)

;; clang-format
(global-set-key (kbd "C-c s") 'clang-format-region)


;; required pkg
(require 'helm-config)
(global-set-key (kbd "M-x") #'helm-M-x)
(global-set-key (kbd "C-x r b") #'helm-filtered-bookmarks)
(global-set-key (kbd "C-x C-f") #'helm-find-files)
(helm-mode 1)

;; Google c style
(require 'google-c-style)
(add-hook 'c-mode-common-hook 'google-set-c-style)
(add-hook 'c-mode-common-hook 'google-make-newline-indent)

;; To make c-basic-offset to 4 for google-c-style
(eval-after-load 'google-c-style
  (dolist (v google-c-style)
	(when (and (listp v) (eq (car v) 'c-basic-offset))
	  (setcdr v 4))))

;(require 'helm-projectile)
;(global-set-key (kbd "C-x p") 'helm-projectile)

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-safe-themes
   (quote
    ("c7f10959cb1bc7a36ee355c765a1768d48929ec55dde137da51077ac7f899521" default))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
