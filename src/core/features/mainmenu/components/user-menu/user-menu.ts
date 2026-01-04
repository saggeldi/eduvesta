// (C) Copyright 2015 Moodle Pty Ltd.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { CoreConstants } from '@/core/constants';
import { CoreSharedModule } from '@/core/shared.module';
import { Component, OnDestroy, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CoreSiteInfo } from '@classes/sites/unauthenticated-site';
import { CoreFilter } from '@features/filter/services/filter';
import { CoreUserAuthenticatedSupportConfig } from '@features/user/classes/support/authenticated-support-config';
import { CoreUserSupport } from '@features/user/services/support';
import { CoreUser, CoreUserProfile } from '@features/user/services/user';
import {
    CoreUserProfileHandlerData,
    CoreUserDelegate,
    CoreUserProfileHandlerType,
    CoreUserDelegateContext,
} from '@features/user/services/user-delegate';
import { CoreModals } from '@services/overlays/modals';
import { CoreNavigator } from '@services/navigator';
import { CoreSites } from '@services/sites';
import { ModalController, Translate } from '@singletons';
import { Subscription } from 'rxjs';
import { CoreLoginHelper } from '@features/login/services/login-helper';
import { CoreSiteLogoComponent } from '@/core/components/site-logo/site-logo';
import { CoreAlerts } from '@services/overlays/alerts';

/**
 * Component to display a modern, beautiful user menu with enhanced animations.
 */
@Component({
    selector: 'core-main-menu-user-menu',
    templateUrl: 'user-menu.html',
    styleUrl: 'user-menu.scss',
    imports: [
        CoreSharedModule,
        CoreSiteLogoComponent,
    ],
})
export class CoreMainMenuUserMenuComponent implements OnInit, OnDestroy {

    @ViewChild('contentElement', { read: ElementRef }) contentElement?: ElementRef;

    siteInfo?: CoreSiteInfo;
    siteUrl?: string;
    displaySiteUrl = false;
    handlers: CoreUserProfileHandlerData[] = [];
    accountHandlers: CoreUserProfileHandlerData[] = [];
    handlersLoaded = false;
    user?: CoreUserProfile;
    displaySwitchAccount = true;
    displayContactSupport = false;
    removeAccountOnLogout = false;

    // Animation states
    isAnimating = false;
    fadeInItems = false;

    protected siteId?: string;
    protected siteName?: string;
    protected subscription!: Subscription;

    /**
     * @inheritdoc
     */
    async ngOnInit(): Promise<void> {
        const currentSite = CoreSites.getRequiredCurrentSite();
        this.siteId = currentSite.getId();
        this.siteInfo = currentSite.getInfo();
        this.siteName = await currentSite.getSiteName();
        this.siteUrl = currentSite.getURL();
        this.displaySwitchAccount = !currentSite.isFeatureDisabled('NoDelegate_SwitchAccount');
        this.displayContactSupport = new CoreUserAuthenticatedSupportConfig(currentSite).canContactSupport();
        this.removeAccountOnLogout = !!CoreConstants.CONFIG.removeaccountonlogout;
        this.displaySiteUrl = currentSite.shouldDisplayInformativeLinks();

        if (!this.siteInfo) {
            return;
        }

        // Trigger fade-in animation after short delay
        setTimeout(() => {
            this.fadeInItems = true;
        }, 100);

        // Load the handlers.
        try {
            this.user = await CoreUser.getProfile(this.siteInfo.userid);
        } catch {
            this.user = {
                id: this.siteInfo.userid,
                fullname: this.siteInfo.fullname,
            };
        }

        this.subscription = CoreUserDelegate.getProfileHandlersFor(this.user, CoreUserDelegateContext.USER_MENU)
            .subscribe((handlers) => {
                if (!this.user) {
                    return;
                }

                let newHandlers = handlers
                    .filter((handler) => handler.type === CoreUserProfileHandlerType.LIST_ITEM)
                    .map((handler) => handler.data);

                // Only update handlers if they have changed, to prevent a blink effect.
                if (newHandlers.length !== this.handlers.length ||
                        JSON.stringify(newHandlers) !== JSON.stringify(this.handlers)) {
                    this.handlers = newHandlers;
                }

                newHandlers = handlers
                    .filter((handler) => handler.type === CoreUserProfileHandlerType.LIST_ACCOUNT_ITEM)
                    .map((handler) => handler.data);

                // Only update handlers if they have changed, to prevent a blink effect.
                if (newHandlers.length !== this.accountHandlers.length ||
                        JSON.stringify(newHandlers) !== JSON.stringify(this.accountHandlers)) {
                    this.accountHandlers = newHandlers;
                }

                this.handlersLoaded = CoreUserDelegate.areHandlersLoaded(this.user.id, CoreUserDelegateContext.USER_MENU);
            });
    }

    /**
     * Opens User profile page with smooth transition.
     *
     * @param event Click event.
     */
    async openUserProfile(event: Event): Promise<void> {
        if (!this.siteInfo || this.isAnimating) {
            return;
        }

        await this.animateItemClick(event);
        await this.close(event);

        CoreNavigator.navigateToSitePath('user/about', {
            params: {
                userId: this.siteInfo.userid,
            },
        });
    }

    /**
     * Opens preferences with smooth transition.
     *
     * @param event Click event.
     */
    async openPreferences(event: Event): Promise<void> {
        if (this.isAnimating) {
            return;
        }

        await this.animateItemClick(event);
        await this.close(event);

        CoreNavigator.navigateToSitePath('preferences');
    }

    /**
     * A handler was clicked with animation.
     *
     * @param event Click event.
     * @param handler Handler that was clicked.
     */
    async handlerClicked(event: Event, handler: CoreUserProfileHandlerData): Promise<void> {
        if (!this.user || this.isAnimating) {
            return;
        }

        await this.animateItemClick(event);
        await this.close(event);

        handler.action(event, this.user, CoreUserDelegateContext.USER_MENU);
    }

    /**
     * Contact site support with animation.
     *
     * @param event Click event.
     */
    async contactSupport(event: Event): Promise<void> {
        if (this.isAnimating) {
            return;
        }

        await this.animateItemClick(event);
        await this.close(event);
        await CoreUserSupport.contact();
    }

    /**
     * Logout the user with confirmation and animation.
     *
     * @param event Click event
     */
    async logout(event: Event): Promise<void> {
        if (this.isAnimating) {
            return;
        }

        if (this.removeAccountOnLogout) {
            // Ask confirm.
            const siteName = this.siteName ?
                await CoreFilter.formatText(this.siteName, { clean: true, singleLine: true, filter: false }, [], this.siteId) :
                '';

            try {
                await CoreAlerts.confirmDelete(Translate.instant('core.login.confirmdeletesite', { sitename: siteName }));
            } catch {
                // User cancelled, stop.
                return;
            }
        }

        await this.animateItemClick(event);
        await this.close(event);

        await CoreSites.logout({
            forceLogout: true,
            removeAccount: this.removeAccountOnLogout,
        });
    }

    /**
     * Show account selector with animation.
     *
     * @param event Click event
     */
    async switchAccounts(event: Event): Promise<void> {
        if (this.isAnimating) {
            return;
        }

        const thisModal = await ModalController.getTop();

        event.preventDefault();
        event.stopPropagation();

        await this.animateItemClick(event);

        const { CoreLoginSitesModalComponent } = await import('@features/login/components/sites-modal/sites-modal');

        const closeAll = await CoreModals.openSideModal<boolean>({
            component: CoreLoginSitesModalComponent,
            cssClass: 'core-modal-lateral core-modal-lateral-sm',
        });

        if (thisModal && closeAll) {
            await ModalController.dismiss(undefined, undefined, thisModal.id);
        }
    }

    /**
     * Add account with animation.
     *
     * @param event Click event
     */
    async addAccount(event: Event): Promise<void> {
        if (this.isAnimating) {
            return;
        }

        await this.animateItemClick(event);
        await this.close(event);

        await CoreLoginHelper.goToAddSite(true, true);
    }

    /**
     * Animate item click for visual feedback.
     *
     * @param event Click event.
     */
    protected async animateItemClick(event: Event): Promise<void> {
        this.isAnimating = true;

        const target = event.target as HTMLElement;
        const item = target.closest('ion-item');

        if (item) {
            // Add scale animation
            item.style.transition = 'transform 0.15s cubic-bezier(0.4, 0, 0.2, 1)';
            item.style.transform = 'scale(0.97)';

            await new Promise(resolve => setTimeout(resolve, 150));

            item.style.transform = 'scale(1)';
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        this.isAnimating = false;
    }

    /**
     * Add haptic feedback for button presses (if available).
     */
    protected triggerHapticFeedback(): void {
        if ('vibrate' in navigator) {
            navigator.vibrate(10);
        }
    }

    /**
     * Close modal with smooth fade-out animation.
     */
    async close(event: Event): Promise<void> {
        event.preventDefault();
        event.stopPropagation();

        // Trigger haptic feedback
        this.triggerHapticFeedback();

        // Add fade-out animation
        if (this.contentElement) {
            const element = this.contentElement.nativeElement;
            element.style.transition = 'opacity 0.2s ease-out';
            element.style.opacity = '0';
            await new Promise(resolve => setTimeout(resolve, 200));
        }

        await ModalController.dismiss();
    }

    /**
     * @inheritdoc
     */
    ngOnDestroy(): void {
        this.subscription?.unsubscribe();
    }

}
