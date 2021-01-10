import { Injectable, SecurityContext } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { map } from 'rxjs/internal/operators';

@Injectable({
  providedIn: 'root',
})
export class StaticHtmlService {
  constructor(
    private httpClient: HttpClient,
    private domSanitizer: DomSanitizer,
  ) {}

  getStaticHTML(url: string, isTrusted: boolean): Observable<string> {
    return this.httpClient.get(url, { responseType: 'text' }).pipe(
      map(response => this.mapStaticHtml(response, isTrusted))
    );
  }

  private mapStaticHtml(htmlString: string, isTrusted: boolean): string {
    return isTrusted ? htmlString : this.domSanitizer.sanitize(SecurityContext.HTML, htmlString);
  }
}
