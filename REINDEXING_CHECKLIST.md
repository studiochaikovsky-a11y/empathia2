# Empathia Village — повторная индексация после обновления

Дата подготовки: 1 октября 2026 года. Выполнять **после** публикации обновлённых файлов на обоих сайтах и проверки, что страницы открываются без старого текста.

## Google Search Console

1. Откройте отдельные подтверждённые ресурсы для `https://empathia-seychelles.com/` и `https://empathiavillage.ru/`.
2. В «Проверке URL» проверьте живую версию и нажмите «Запросить индексирование» для приоритетных страниц ниже. Запрос не гарантирует мгновенного попадания в индекс.
3. В разделе «Файлы Sitemap» проверьте `https://empathia-seychelles.com/sitemap.xml` и `https://empathiavillage.ru/sitemap.xml`. Если карты ещё не добавлены — добавьте. Если добавлены — проверьте дату последнего чтения и ошибки; при необходимости отправьте адрес карты повторно. Не загружайте PDF вместо XML-карты.
4. Через 1–2 недели проверьте выбранный Google canonical, дату обхода и данные в сниппете. При обнаружении старых сведений проверьте живую страницу и повторный обход.

Приоритетные английские URL:

- `https://empathia-seychelles.com/`
- `https://empathia-seychelles.com/pricing`
- `https://empathia-seychelles.com/faq`
- `https://empathia-seychelles.com/project-facts`
- `https://empathia-seychelles.com/buyer-due-diligence.html`
- `https://empathia-seychelles.com/seychelles-residency-by-investment`
- `https://empathia-seychelles.com/construction`

Приоритетные русские URL:

- `https://empathiavillage.ru/`
- `https://empathiavillage.ru/pricing.html`
- `https://empathiavillage.ru/faq.html`
- `https://empathiavillage.ru/project-facts.html`
- `https://empathiavillage.ru/kak-kupit-nedvizhimost-na-seychelah.html`
- `https://empathiavillage.ru/construction.html`
- `https://empathiavillage.ru/masterplan.html`

## Яндекс Вебмастер

1. Для каждого домена откройте «Индексирование → Переобход страниц» и отправьте соответствующие приоритетные URL.
2. В «Индексирование → Файлы Sitemap» проверьте обработку актуальных карт. Если адрес уже добавлен, **удалять и загружать заново не требуется**: Яндекс переобрабатывает обновлённый файл. При необходимости используйте доступную команду повторного обхода карты.
3. Проверьте «Страницы в поиске», дату обхода и сниппеты. Старые URL, которые перенаправлены, должны отдавать HTTP 301; URL удалённых страниц не должны оставаться в актуальной sitemap.

## Старый домен `empathia-village.com`

- После настройки перенаправления на хостинге проверьте HTTP-статус **301**, заголовок `Location` и конечную страницу для `/` и каждого известного старого URL. JavaScript-перенаправление не подходит.
- Подтвердите в Google Search Console и Яндекс Вебмастере права на старый домен; отслеживайте, когда старые страницы будут заменены в индексе актуальными адресами.
- До настройки 301 старый домен **остаётся источником неверных цен и обещаний**. Переобход новых сайтов не исправит его сам по себе.

Официальные инструкции: [Google — Проверка URL](https://support.google.com/webmasters/answer/9012289?hl=ru), [Яндекс — файлы Sitemap](https://yandex.com/support/webmaster/en/indexing-options/sitemap), [Яндекс — новые и изменённые страницы](https://www.yandex.com/support/webmaster/en/robot-workings/new-changed).
