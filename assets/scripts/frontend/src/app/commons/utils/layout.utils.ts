// import { NavComponent } from '../../components/partials/nav/nav.component';
/* CONTENT ONLY LAYOUT
 * @desc : web layout view that only loads the
 *         content fully. (no navs, footer, sidebar, etc..)
 */
export function ContentOnly(content) {
  return { content };
}

/* USER NAVIGATION, CONTENT
* @desc : web layout view that preloads the navigation bar
*         together with the content.
*/
// export function NavContent(content) {
//   return {
//     nav: NavComponent,
//     content
//   };
// }
